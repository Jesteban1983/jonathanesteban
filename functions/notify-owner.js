// === NETLIFY SERVERLESS FUNCTION: NOTIFY OWNER VIA TELEGRAM ===

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
  const telegramChatId = process.env.TELEGRAM_CHAT_ID;

  if (!telegramToken || !telegramChatId) {
    return { statusCode: 200, body: JSON.stringify({ message: 'Telegram credentials missing' }) };
  }

  const { title, details } = JSON.parse(event.body);

  await fetch(`https://api.telegram.org/bot${telegramToken}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: telegramChatId,
      text: `🚨 *${title || 'Alerta de Sistema'}*\n\n${details || ''}`,
      parse_mode: 'Markdown'
    })
  });

  return { statusCode: 200, body: JSON.stringify({ sent: true }) };
};
