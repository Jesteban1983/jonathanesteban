// ═══════════════════════════════════════════════════════════════════════
// contact-recepcionista.js — Fase 1 · Recepcionista AI (jonathanesteban.dev)
// ───────────────────────────────────────────────────────────────────────
// Punto de entrada del formulario de contacto.
// Hace de PROXY seguro hacia el webhook n8n del recepcionista, y solo eso:
//  • Honeypot anti-bots (server-side, re-verificación)
//  • Rate-limit persistente (Netlify Blobs) — 3 envíos / 5 min por IP
//  • Validación de campos requeridos (mínima, el agente n8n hace la lectura)
//  • POST al webhook n8n con secreto compartido en header (nunca en el body)
//
// El cliente SIEMPRE cae a Formspree si esta función no responde 200
// (ver contacto/index.astro). Así la producción nunca se rompe.
//
// Variables de entorno (Netlify UI o `netlify dev` con .env en astro-portfolio/):
//   N8N_WEBHOOK_LEADS_URL  → https://n8n.jonathanesteban.dev/webhook/recepcionista-leads
//   N8N_WEBHOOK_SECRET     → secreto compartido (mismo valor en n8n)
// ═══════════════════════════════════════════════════════════════════════

const WEBHOOK_URL = process.env.N8N_WEBHOOK_LEADS_URL || '';
const WEBHOOK_SECRET = process.env.N8N_WEBHOOK_SECRET || '';

// Ventana de rate-limit (ms) y máx de envíos por IP dentro de la ventana.
const RATE_WINDOW_MS = 5 * 60 * 1000; // 5 minutos
const RATE_MAX = 3;                  // 3 envíos por IP

const requiredFields = ['name', 'email', 'message'];

// ── Netlify Blobs (persistente entre invocaciones serverless) ──────────
// Netlify Functions resuelve `@netlify/blobs` desde el runtime; no hace
// falta instalarlo. Si no está disponible, caemos a un rate-limit en
// memoria (mejor que nada, pero no compartido entre invocaciones).
let blobsAvailable = null;

async function getBlobStore() {
  if (blobsAvailable !== null) return blobsAvailable;
  try {
    const { getStore } = await import('@netlify/blobs');
    blobsAvailable = getStore('recepcionista');
  } catch (err) {
    blobsAvailable = false;
  }
  return blobsAvailable;
}

function clientIp(event) {
  const fwd = event.headers['x-nf-client-connection-ip']
    || event.headers['x-forwarded-for']
    || '';
  return (fwd.split(',')[0] || 'unknown').trim().slice(0, 64);
}

// ── Rate limit ─────────────────────────────────────────────────────────
async function checkRateLimit(ip) {
  const key = `rate-${ip}`;
  const now = Date.now();
  const store = await getBlobStore();

  if (store) {
    const raw = await store.get(key, { type: 'json' }).catch(() => null);
    const rec = raw && raw.windowStart && now - raw.windowStart < RATE_WINDOW_MS
      ? raw
      : { windowStart: now, count: 0 };
    rec.count += 1;
    await store.setJSON(key, rec, { ttl: RATE_WINDOW_MS / 1000 }).catch(() => {});
    return { allowed: rec.count <= RATE_MAX, retryAfterSeconds: Math.ceil((rec.windowStart + RATE_WINDOW_MS - now) / 1000) };
  }

  // Fallback en memoria (no compartido entre instancias)
  globalThis.__rateMap = globalThis.__rateMap || new Map();
  const rec = globalThis.__rateMap.get(key);
  const fresh = rec && now - rec.windowStart < RATE_WINDOW_MS ? rec : { windowStart: now, count: 0 };
  fresh.count += 1;
  globalThis.__rateMap.set(key, fresh);
  return { allowed: fresh.count <= RATE_MAX, retryAfterSeconds: Math.ceil((fresh.windowStart + RATE_WINDOW_MS - now) / 1000) };
}

function parseBody(event) {
  let raw = event.body || '';
  if (event.isBase64Encoded) {
    try {
      raw = Buffer.from(raw, 'base64').toString('utf8');
    } catch {}
  }
  const ct = (event.headers['content-type'] || '').toLowerCase();
  try {
    if (ct.includes('application/json')) return JSON.parse(raw);
    if (ct.includes('application/x-www-form-urlencoded')) {
      return Object.fromEntries(new URLSearchParams(raw));
    }
    // Si viene como multipart/form-data
    if (ct.includes('multipart/form-data') || raw.includes('Content-Disposition: form-data')) {
      const result = {};
      const matches = raw.matchAll(/name="([^"]+)"\r?\n\r?\n([\s\S]*?)\r?\n--/g);
      for (const match of matches) {
        result[match[1]] = match[2].trim();
      }
      if (Object.keys(result).length > 0) return result;
    }
    try { return JSON.parse(raw); } catch { /* siguiente intento */ }
    return Object.fromEntries(new URLSearchParams(raw));
  } catch (err) {
    return {};
  }
}

function jsonOk(obj) {
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(obj),
  };
}

function jsonBad(status, msg) {
  return {
    statusCode: status,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ok: false, error: msg }),
  };
}

export const handler = async (event) => {
  // 1) Solo POST
  if (event.httpMethod !== 'POST') {
    return jsonBad(405, 'Method Not Allowed');
  }

  // 2) Honeypot: si un bot rellenó los campos ocultos, fingimos éxito y
  //    NO reenviamos nada. Silencioso para no educar a los bots.
  const body = parseBody(event);
  const gotcha = String(body._gotcha || '').trim();
  const companySite = String(body.company_site || '').trim();
  if (gotcha !== '' || companySite !== '') {
    return jsonOk({ ok: true, honeypot: true });
  }

  // 3) Rate-limit por IP
  const ip = clientIp(event);
  const rate = await checkRateLimit(ip);
  if (!rate.allowed) {
    return {
      statusCode: 429,
      headers: {
        'Content-Type': 'application/json',
        'Retry-After': String(rate.retryAfterSeconds),
      },
      body: JSON.stringify({ ok: false, error: 'Demasiados envíos. Inténtalo en unos minutos.' }),
    };
  }

  // 4) Validación de campos mínimos
  for (const field of requiredFields) {
    if (!String(body[field] || '').trim()) {
      return jsonBad(400, `Falta el campo: ${field}`);
    }
  }
  const email = String(body.email).trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return jsonBad(400, 'Correo electrónico no válido');
  }
  const message = String(body.message).trim();
  if (message.length > 4000) {
    return jsonBad(400, 'Mensaje demasiado largo (máx. 4000 caracteres)');
  }

  // 5) Construcción del payload limpio del lead
  const payload = {
    source: 'web-form',
    submittedAt: new Date().toISOString(),
    name: String(body.name).trim(),
    email,
    subject: String(body.subject || '').trim(),
    message,
    consentWhatsapp: body.consentWhatsapp === 'on' || body.consentWhatsapp === true || body.consentWhatsapp === 'true',
    ip,
  };

  // Registrar siempre en los logs de Netlify Functions para trazabilidad inmediata
  console.log('[RECEPCIONISTA] Nuevo lead recibido:', JSON.stringify(payload));

  // 6) Guardar en Netlify Blobs si está disponible (persistencia serverless)
  try {
    const store = await getBlobStore();
    if (store) {
      const leadId = `lead-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
      await store.setJSON(leadId, payload);
    }
  } catch (blobErr) {
    console.warn('[recepcionista] Netlify Blobs aviso:', blobErr.message);
  }

  // 7) Notificación por email si hay RESEND_API_KEY configurada
  if (process.env.RESEND_API_KEY) {
    try {
      const ownerEmail = process.env.OWNER_EMAIL || 'contacto@jonathanesteban.dev';
      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: 'Jonathan Esteban Portfolio <onboarding@resend.dev>',
          to: [ownerEmail],
          reply_to: email,
          subject: `[Nuevo Contacto Web] ${payload.subject || 'Incidencia'} - ${payload.name}`,
          html: `
            <h2>Nuevo mensaje desde jonathanesteban.dev</h2>
            <p><strong>Nombre:</strong> ${payload.name}</p>
            <p><strong>Email:</strong> ${payload.email}</p>
            <p><strong>Asunto:</strong> ${payload.subject || 'Sin especificar'}</p>
            <p><strong>WhatsApp consent:</strong> ${payload.consentWhatsapp ? 'Sí' : 'No'}</p>
            <p><strong>Mensaje:</strong></p>
            <blockquote style="background:#f4f4f4;padding:12px;border-left:4px solid #0052cc;">
              ${payload.message.replace(/\n/g, '<br>')}
            </blockquote>
            <p><small>Fecha: ${payload.submittedAt} · IP: ${payload.ip}</small></p>
          `
        })
      });
    } catch (mailErr) {
      console.error('[recepcionista] Error enviando email con Resend:', mailErr);
    }
  }

  // 8) Reenvío al webhook n8n (si está configurada la URL)
  if (WEBHOOK_URL) {
    try {
      const n8nRes = await fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-n8n-secret': WEBHOOK_SECRET,
        },
        body: JSON.stringify(payload),
      });

      if (!n8nRes.ok) {
        console.warn('[recepcionista] n8n respondió status', n8nRes.status);
      }
    } catch (err) {
      console.error('[recepcionista] error llamando a n8n:', err.message);
    }
  }

  // Confirmar éxito para que el cliente redirija a /gracias/
  return jsonOk({ ok: true });
};