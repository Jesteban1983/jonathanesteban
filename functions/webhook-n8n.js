// === NETLIFY SERVERLESS FUNCTION: SECURE PROXY TO N8N WORKFLOWS ===

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const n8nUrl = process.env.N8N_WEBHOOK_LEADS_URL;
  if (!n8nUrl) {
    return { statusCode: 500, body: JSON.stringify({ error: 'n8n URL not configured' }) };
  }

  try {
    const payload = JSON.parse(event.body);

    const response = await fetch(n8nUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Webhook-Secret': process.env.N8N_WEBHOOK_SECRET || ''
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, data: data })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'n8n relay error' })
    };
  }
};
