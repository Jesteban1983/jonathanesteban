// === NETLIFY SERVERLESS FUNCTION: META/FACEBOOK OAUTH TOKEN EXCHANGE ===

exports.handler = async (event) => {
  const code = event.queryStringParameters.code;

  if (!code) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing authorization code' })
    };
  }

  const appId = process.env.FACEBOOK_APP_ID;
  const appSecret = process.env.FACEBOOK_APP_SECRET;
  const redirectUri = process.env.FACEBOOK_REDIRECT_URI || 'https://jonathanesteban.dev/auth/facebook/callback/';

  try {
    const tokenUrl = `https://graph.facebook.com/v19.0/oauth/access_token?client_id=${appId}&redirect_uri=${encodeURIComponent(redirectUri)}&client_secret=${appSecret}&code=${code}`;
    
    const response = await fetch(tokenUrl);
    const data = await response.json();

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, message: 'Facebook OAuth exchange successful', data: data })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Facebook OAuth Exchange Failed' })
    };
  }
};
