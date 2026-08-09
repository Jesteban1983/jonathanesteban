// === NETLIFY SERVERLESS FUNCTION: TIKTOK OAUTH TOKEN EXCHANGE ===

exports.handler = async (event) => {
  const code = event.queryStringParameters.code;

  if (!code) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing authorization code' })
    };
  }

  const clientKey = process.env.TIKTOK_CLIENT_KEY;
  const clientSecret = process.env.TIKTOK_CLIENT_SECRET;
  const redirectUri = process.env.TIKTOK_REDIRECT_URI || 'https://jonathanesteban.dev/auth/tiktok/callback/';

  try {
    const tokenResponse = await fetch('https://open.tiktokapis.com/v2/oauth/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_key: clientKey,
        client_secret: clientSecret,
        code: code,
        grant_type: 'authorization_code',
        redirect_uri: redirectUri
      })
    });

    const data = await tokenResponse.json();

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, message: 'OAuth exchange successful', data: data })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'TikTok OAuth Exchange Failed' })
    };
  }
};
