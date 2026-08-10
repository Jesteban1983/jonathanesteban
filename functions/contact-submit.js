// === NETLIFY SERVERLESS FUNCTION: CONTACT FORM SUBMISSION ===
// Validación → Email al propietario + Auto-respuesta al usuario + Telegram + n8n
// Todo integrado en UNA función serverless. Sin dependencias npm (usa fetch nativo).

const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutos
const RATE_LIMIT_MAX = 8;
const OWNER_EMAIL = 'joonathanesteban@gmail.com';
const SITE_URL = 'https://jonathanesteban.dev';

// ── Cache de rate limiting (en caliente, se pierde al cold-start pero reinicia) ──
const requestLog = new Map();

function getClientId(event) {
  const headers = event.headers || {};
  return (
    headers['x-forwarded-for'] ||
    headers['client-ip'] ||
    headers['x-nf-client-connection-ip'] ||
    'unknown'
  ).split(',')[0].trim();
}

function isRateLimited(clientId) {
  const now = Date.now();
  const hits = requestLog.get(clientId) || [];
  const freshHits = hits.filter((ts) => now - ts < RATE_LIMIT_WINDOW_MS);
  freshHits.push(now);
  requestLog.set(clientId, freshHits);
  return freshHits.length > RATE_LIMIT_MAX;
}

// ── Envío de email con doble proveedor ────────────────────────────────────
async function sendEmail({ to, subject, html, replyTo }) {
  const resendKey = process.env.RESEND_API_KEY;
  const sendgridKey = process.env.SENDGRID_API_KEY;
  const senderName = 'Jonathan Esteban';
  const senderEmail = process.env.SENDER_EMAIL_NO_REPLY || 'joonathanesteban@gmail.com';
  const errors = [];

  // Intentar con Resend (primario)
  if (resendKey) {
    try {
      const body = {
        from: `${senderName} <onboarding@resend.dev>`, // Con dominio verificado se cambia
        to: [to],
        subject,
        html,
        reply_to: replyTo || senderEmail
      };

      // Si tiene dominio verificado, usar ese
      const resendDomain = process.env.RESEND_DOMAIN;
      if (resendDomain) {
        body.from = `${senderName} <contacto@${resendDomain}>`;
      }

      const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${resendKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });

      if (res.ok) {
        return { ok: true, provider: 'resend' };
      }
      const errBody = await res.text();
      errors.push(`Resend (status ${res.status}): ${errBody}`);
    } catch (err) {
      errors.push(`Resend error: ${err.message}`);
    }
  }

  // Fallback a SendGrid si Resend no está configurado o falló
  if (sendgridKey) {
    try {
      const res = await fetch('https://api.sendgrid.com/v3/mail/send', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${sendgridKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          personalizations: [{ to: [{ email: to }], reply_to: replyTo ? { email: replyTo } : undefined }],
          from: { email: senderEmail, name: senderName },
          subject,
          content: [{ type: 'text/html', value: html }]
        })
      });

      if (res.ok) {
        return { ok: true, provider: 'sendgrid' };
      }
      const errBody = await res.text();
      errors.push(`SendGrid (status ${res.status}): ${errBody}`);
    } catch (err) {
      errors.push(`SendGrid error: ${err.message}`);
    }
  }

  // Ninguno configurado o ambos fallaron
  if (!resendKey && !sendgridKey) {
    return { ok: false, error: 'No email provider configured (set RESEND_API_KEY or SENDGRID_API_KEY)' };
  }

  return { ok: false, errors };
}

// ── Handlers de email ─────────────────────────────────────────────────────

function buildOwnerEmailHtml(data) {
  const { name, email, phone, service, businessType, budget, timeline, safeSubject, safeMessage, consentWhatsapp } = data;
  const serviceLabels = {
    'desarrollo-web': 'Desarrollo Web',
    'automatizacion': 'Automatización y agentes IA',
    'soporte-it': 'Soporte IT',
    'otro': 'Otro'
  };
  const serviceLabel = serviceLabels[service] || service;

  return `<!DOCTYPE html>
<html><body style="font-family: Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
<div style="background: #0a0a0a; color: #f5f5f5; padding: 30px; border-radius: 12px;">
  <div style="text-align: center; margin-bottom: 24px;">
    <h1 style="margin: 0; font-size: 22px; color: #f5f5f5;">📬 Nuevo Lead</h1>
    <p style="color: #888; font-size: 14px;">${SITE_URL} — ${new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
  </div>
  <table style="width: 100%; border-collapse: collapse; font-size: 15px;">
    <tr><td style="padding: 8px 12px; color: #888; width: 120px; vertical-align: top;">👤 Nombre</td><td style="padding: 8px 12px; color: #f5f5f5;"><strong>${name}</strong></td></tr>
    <tr style="background: #141414;"><td style="padding: 8px 12px; color: #888; vertical-align: top;">✉️ Email</td><td style="padding: 8px 12px; color: #f5f5f5;"><a href="mailto:${email}" style="color: #60a5fa;">${email}</a></td></tr>
    ${phone ? `<tr><td style="padding: 8px 12px; color: #888; vertical-align: top;">📞 Teléfono</td><td style="padding: 8px 12px; color: #f5f5f5;"><a href="tel:${phone}" style="color: #60a5fa;">${phone}</a></td></tr>` : ''}
    <tr${phone ? ' style="background: #141414;"' : ''}><td style="padding: 8px 12px; color: #888; vertical-align: top;">🧩 Servicio</td><td style="padding: 8px 12px; color: #f5f5f5;">${serviceLabel}</td></tr>
    <tr style="background: #141414;"><td style="padding: 8px 12px; color: #888; vertical-align: top;">🏢 Negocio</td><td style="padding: 8px 12px; color: #f5f5f5;">${businessType}</td></tr>
    <tr><td style="padding: 8px 12px; color: #888; vertical-align: top;">💶 Presupuesto</td><td style="padding: 8px 12px; color: #f5f5f5;">${budget}</td></tr>
    <tr style="background: #141414;"><td style="padding: 8px 12px; color: #888; vertical-align: top;">⏱️ Plazo</td><td style="padding: 8px 12px; color: #f5f5f5;">${timeline}</td></tr>
    ${safeSubject ? `<tr><td style="padding: 8px 12px; color: #888; vertical-align: top;">📌 Asunto</td><td style="padding: 8px 12px; color: #f5f5f5;">${safeSubject}</td></tr>` : ''}
  </table>
  <div style="margin-top: 16px; padding: 16px; background: #141414; border-radius: 8px;">
    <h3 style="margin: 0 0 8px; font-size: 14px; color: #888;">📝 Mensaje</h3>
    <p style="margin: 0; color: #f5f5f5; line-height: 1.5; white-space: pre-wrap;">${safeMessage}</p>
  </div>
  <div style="margin-top: 16px; padding: 12px 16px; background: #141414; border-radius: 8px; font-size: 13px; color: #888;">
    ✅ Consentimiento respuesta: Sí
    <br>💬 Consentimiento WhatsApp: ${consentWhatsapp ? 'Sí' : 'No'}
  </div>
  <div style="margin-top: 24px; text-align: center;">
    <a href="mailto:${email}" style="display: inline-block; padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">✉️ Responder a ${name}</a>
  </div>
</div></body></html>`;
}

function buildAutoresponseHtml(name) {
  return `<!DOCTYPE html>
<html><body style="font-family: Helvetica, Arial, sans-serif; max-width: 560px; margin: 0 auto; padding: 24px; background: #f9f9f9;">
<div style="background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
  <div style="background: linear-gradient(135deg, #0a0a0a, #1e293b); padding: 32px; text-align: center;">
    <h1 style="margin: 0; color: #ffffff; font-size: 22px;">¡Mensaje recibido! ✅</h1>
  </div>
  <div style="padding: 32px;">
    <p style="font-size: 16px; color: #333; line-height: 1.6;">Hola <strong style="color: #0a0a0a;">${name}</strong>,</p>
    <p style="font-size: 15px; color: #555; line-height: 1.6;">Gracias por ponerte en contacto a través de mi web. He recibido tu consulta y la revisaré personalmente.</p>
    <p style="font-size: 15px; color: #555; line-height: 1.6;">Me pondré en contacto contigo en <strong>menos de 24 horas</strong> para resolver tus dudas y darte un presupuesto adaptado a tu proyecto.</p>
    <div style="margin: 24px 0; padding: 16px; background: #f0f9ff; border-left: 4px solid #2563eb; border-radius: 4px;">
      <p style="margin: 0; font-size: 14px; color: #333; line-height: 1.5;">
        ⏱️ Si tu consulta es urgente, puedes escribirme directamente por 
        <a href="https://wa.me/34614739345" style="color: #2563eb; font-weight: 600;">WhatsApp</a>.
      </p>
    </div>
    <p style="font-size: 15px; color: #555; line-height: 1.6;">Un cordial saludo,</p>
    <p style="font-size: 16px; color: #0a0a0a; line-height: 1.4; margin-bottom: 4px;"><strong>Jonathan Esteban Barona</strong></p>
    <p style="font-size: 14px; color: #888; margin-top: 0;">Full-Stack Developer & AI Engineer</p>
    <p style="font-size: 13px; color: #888;">
      <a href="${SITE_URL}" style="color: #2563eb;">${SITE_URL}</a> · 
      <a href="${SITE_URL}/privacy-policy/" style="color: #888;">Política de Privacidad</a>
    </p>
  </div>
</div></body></html>`;
}

// ── Handler principal ─────────────────────────────────────────────────────

exports.handler = async (event) => {
  // Solo POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

  // Rate limiting por IP
  const clientId = getClientId(event);
  if (isRateLimited(clientId)) {
    return {
      statusCode: 429,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Demasiadas solicitudes. Inténtalo en unos minutos.' })
    };
  }

  try {
    const payload = JSON.parse(event.body);

    // Honeypot antispam
    if (payload.company_site) {
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    }

    // ── Extraer y sanitizar ──
    const {
      name, email, phone, service, businessType,
      budget, timeline, subject, message,
      consentReply, consentWhatsapp
    } = payload;

    const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // ── Validaciones ──
    const camposFaltantes = [];
    if (!name) camposFaltantes.push('nombre');
    if (!email) camposFaltantes.push('email');
    if (!service) camposFaltantes.push('servicio');
    if (!businessType) camposFaltantes.push('tipo de negocio');
    if (!budget) camposFaltantes.push('presupuesto');
    if (!timeline) camposFaltantes.push('plazo');
    if (!message) camposFaltantes.push('mensaje');

    if (camposFaltantes.length > 0) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: `Faltan campos obligatorios: ${camposFaltantes.join(', ')}` })
      };
    }

    if (!EMAIL_REGEX.test(email)) {
      return { statusCode: 400, body: JSON.stringify({ error: 'El correo electrónico no es válido' }) };
    }

    if (String(message).length > 2000) {
      return { statusCode: 400, body: JSON.stringify({ error: 'El mensaje supera el límite de 2000 caracteres' }) };
    }

    if (consentReply !== true) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Debes aceptar el consentimiento para recibir respuesta' }) };
    }

    // Sanitizar
    const safeMessage = String(message).replace(/[<>]/g, '');
    const safeSubject = String(subject || '').replace(/[<>]/g, '');

    // ── Enviar notificaciones en paralelo ──
    const emailPromises = [];
    const notifyPromises = [];

    const emailData = { name, email, phone, service, businessType, budget, timeline, safeSubject, safeMessage, consentWhatsapp };

    // 1. Email al propietario
    emailPromises.push(
      sendEmail({
        to: OWNER_EMAIL,
        subject: `📬 Nuevo lead: ${name} — ${service}`,
        html: buildOwnerEmailHtml(emailData),
        replyTo: email
      })
    );

    // 2. Auto-respuesta al usuario
    emailPromises.push(
      sendEmail({
        to: email,
        subject: '✅ Recibí tu mensaje — Jonathan Esteban',
        html: buildAutoresponseHtml(name)
      })
    );

    // 3. Telegram
    const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
    const telegramChatId = process.env.TELEGRAM_CHAT_ID;
    if (telegramToken && telegramChatId) {
      const text = `📬 *Nuevo Lead*\n👤 ${name}\n✉️ ${email}\n🧩 ${service}\n🏢 ${businessType}\n💶 ${budget}\n📝 ${safeMessage.substring(0, 200)}${safeMessage.length > 200 ? '…' : ''}`;
      notifyPromises.push(
        fetch(`https://api.telegram.org/bot${telegramToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: telegramChatId, text, parse_mode: 'Markdown' })
        }).catch(err => console.error('Telegram error:', err.message))
      );
    }

    // 4. n8n webhook
    const n8nWebhook = process.env.N8N_WEBHOOK_LEADS_URL;
    if (n8nWebhook) {
      notifyPromises.push(
        fetch(n8nWebhook, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Webhook-Secret': process.env.N8N_WEBHOOK_SECRET || ''
          },
          body: JSON.stringify({
            name, email, phone, service, businessType, budget, timeline,
            subject: safeSubject,
            message: safeMessage,
            consentReply, consentWhatsapp,
            timestamp: new Date().toISOString(),
            sourceUrl: SITE_URL
          })
        }).catch(err => console.error('n8n error:', err.message))
      );
    }

    // Esperar a todos (errores capturados individualmente)
    const emailResults = await Promise.allSettled(emailPromises);
    await Promise.allSettled(notifyPromises);

    // Verificar si al menos un email se envió correctamente
    const emailOk = emailResults.some(r => r.status === 'fulfilled' && r.value && r.value.ok === true);
    const emailErrors = emailResults
      .filter(r => r.status === 'fulfilled' && r.value && r.value.errors)
      .flatMap(r => r.value.errors);

    if (!emailOk && emailErrors.length > 0) {
      console.error('Email errors:', emailErrors.join(' | '));
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        message: 'Mensaje enviado correctamente',
        emailSent: emailOk
      })
    };

  } catch (error) {
    console.error('Contact Submit Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Error interno del servidor. Inténtalo de nuevo más tarde.' })
    };
  }
};
