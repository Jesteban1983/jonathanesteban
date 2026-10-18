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
  const raw = event.body || '';
  const ct = event.headers['content-type'] || '';
  try {
    if (ct.includes('application/json')) return JSON.parse(raw);
    if (ct.includes('application/x-www-form-urlencoded')) {
      return Object.fromEntries(new URLSearchParams(raw));
    }
    // Intentar JSON aunque no venga el header (fetch con body formData a veces)
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

  // 5) No hay webhook configurado → devolver 503 para que el cliente
  //    caiga a Formspree (fallback controlado, sin romper el resto).
  if (!WEBHOOK_URL) {
    return jsonBad(503, 'webhook n8n no configurado');
  }

  // 6) Payload limpio hacia n8n (solo datos del cliente, NADA de env/secretos)
  const payload = {
    source: 'web-form',
    submittedAt: new Date().toISOString(),
    name: String(body.name).trim(),
    email,
    subject: String(body.subject || '').trim(),
    message,
    consentWhatsapp: body.consentWhatsapp === 'on' || body.consentWhatsapp === true,
  };

  // 7) Llamada al webhook n8n con secreto en header
  try {
    const n8nRes = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-n8n-secret': WEBHOOK_SECRET,
      },
      body: JSON.stringify(payload),
    });

    // El webhook n8n responde 200 si aceptó; cualquier otra cosa → fallback
    if (!n8nRes.ok) {
      console.error('[recepcionista] n8n respondió', n8nRes.status);
      return jsonBad(502, 'El servicio de procesamiento no respondió correctamente');
    }
    return jsonOk({ ok: true });
  } catch (err) {
    console.error('[recepcionista] error llamando a n8n:', err);
    return jsonBad(502, 'El servicio de procesamiento no está disponible');
  }
};