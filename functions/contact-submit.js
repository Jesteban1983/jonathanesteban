// === NETLIFY SERVERLESS FUNCTION: CONTACT FORM SUBMISSION ===

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

  try {
    const payload = JSON.parse(event.body);

    // Bot detection check (honeypot field)
    if (payload._gotcha) {
      return { statusCode: 200, body: JSON.stringify({ success: true, message: 'Received' }) };
    }

    const { name, email, subject, message } = payload;

    if (!name || !email || !message) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Faltan campos obligatorios' }) };
    }

    // Process notification via Telegram if bot token configured
    const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
    const telegramChatId = process.env.TELEGRAM_CHAT_ID;

    if (telegramToken && telegramChatId) {
      const text = `📬 *Nuevo Lead en jonathanesteban.dev*\n\n👤 *Nombre:* ${name}\n✉️ *Email:* ${email}\n📌 *Asunto:* ${subject || 'Contacto General'}\n📝 *Mensaje:* ${message}`;
      
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
        body: JSON.stringify({ name, email, subject, message, timestamp: new Date().toISOString() })
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
