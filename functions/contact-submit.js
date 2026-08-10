// === NETLIFY SERVERLESS FUNCTION: CONTACT FORM SUBMISSION ===

const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000;
const RATE_LIMIT_MAX = 8;
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

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

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

    // Bot detection check (honeypot field)
    if (payload.company_site) {
      return { statusCode: 200, body: JSON.stringify({ success: true, message: 'Received' }) };
    }

    const {
      name,
      email,
      phone,
      service,
      businessType,
      budget,
      timeline,
      subject,
      message,
      consentReply,
      consentWhatsapp
    } = payload;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!name || !email || !service || !businessType || !budget || !timeline || !message) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Faltan campos obligatorios' }) };
    }

    if (!emailRegex.test(email)) {
      return { statusCode: 400, body: JSON.stringify({ error: 'El correo electrónico no es válido' }) };
    }

    if (String(message).length > 2000) {
      return { statusCode: 400, body: JSON.stringify({ error: 'El mensaje supera el tamaño permitido' }) };
    }

    if (consentReply !== true) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Debes aceptar el consentimiento para responderte' }) };
    }

    const safeMessage = String(message).replace(/[<>]/g, '');
    const safeSubject = String(subject || 'Contacto General').replace(/[<>]/g, '');

    // Process notification via Telegram if bot token configured
    const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
    const telegramChatId = process.env.TELEGRAM_CHAT_ID;

    if (telegramToken && telegramChatId) {
      const text = `📬 *Nuevo Lead en jonathanesteban.dev*\n\n👤 *Nombre:* ${name}\n✉️ *Email:* ${email}\n📞 *Telefono:* ${phone || 'No informado'}\n🧩 *Servicio:* ${service}\n🏢 *Negocio:* ${businessType}\n💶 *Presupuesto:* ${budget}\n⏱️ *Plazo:* ${timeline}\n📌 *Asunto:* ${safeSubject}\n📝 *Mensaje:* ${safeMessage}\n✅ *Consentimiento respuesta:* ${consentReply ? 'Si' : 'No'}\n💬 *Consentimiento WhatsApp:* ${consentWhatsapp ? 'Si' : 'No'}`;
      
      await fetch(`https://api.telegram.org/bot${telegramToken}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: telegramChatId, text: text, parse_mode: 'Markdown' })
      }).catch(err => console.error('Telegram notification error:', err));
    }

    // Forward lead data to n8n webhook if configured
    const n8nWebhook = process.env.N8N_WEBHOOK_LEADS_URL;
    if (n8nWebhook) {
      await fetch(n8nWebhook, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Secret': process.env.N8N_WEBHOOK_SECRET || ''
        },
        body: JSON.stringify({
          name,
          email,
          phone,
          service,
          businessType,
          budget,
          timeline,
          subject: safeSubject,
          message: safeMessage,
          consentReply,
          consentWhatsapp,
          timestamp: new Date().toISOString()
        })
      }).catch(err => console.error('n8n webhook error:', err));
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, message: 'Mensaje enviado correctamente' })
    };
  } catch (error) {
    console.error('Contact Submit Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Error interno al procesar el contacto' })
    };
  }
};
