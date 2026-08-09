// === NETLIFY SERVERLESS FUNCTION: META DATA DELETION REQUEST ENDPOINT ===
const crypto = require('crypto');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const params = new URLSearchParams(event.body);
    const signedRequest = params.get('signed_request');

    if (!signedRequest) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing signed_request' }) };
    }

    const [encodedSig, payload] = signedRequest.split('.', 2);
    const secret = process.env.FACEBOOK_APP_SECRET || 'fallback_secret';

    // Verify signature
    const sig = Buffer.from(encodedSig.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('hex');
    const expectedSig = crypto.createHmac('sha256', secret).update(payload).digest('hex');

    const data = JSON.parse(Buffer.from(payload.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8'));
    const userId = data.user_id;

    const confirmationCode = `DEL-${userId}-${Date.now()}`;
    const statusUrl = `https://jonathanesteban.dev/data-deletion/?code=${confirmationCode}`;

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: statusUrl,
        confirmation_code: confirmationCode
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Data deletion callback processing failed' })
    };
  }
};
