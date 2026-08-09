// === NETLIFY SERVERLESS FUNCTION: AUTORESPONSE EMAIL ===

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const sendgridKey = process.env.SENDGRID_API_KEY;
  if (!sendgridKey) {
    return { statusCode: 200, body: JSON.stringify({ message: 'SendGrid key not configured' }) };
  }

  const { email, name } = JSON.parse(event.body);

  const emailData = {
    personalizations: [{ to: [{ email: email, name: name }] }],
    from: { email: process.env.SENDER_EMAIL_NO_REPLY || 'joonathanesteban@gmail.com', name: 'Jonathan Esteban' },
    subject: '¡Hemos recibido tu mensaje correctamente! — Jonathan Esteban',
    content: [{
      type: 'text/html',
      value: `<p>Hola <strong>${name}</strong>,</p><p>Muchas gracias por ponerte en contacto. He recibido tu mensaje y me pondré en contacto contigo en menos de 24 horas.</p><p>Un cordial saludo,<br><strong>Jonathan Esteban Barona</strong><br>Full-Stack Developer & AI Engineer<br><a href="https://jonathanesteban.dev">jonathanesteban.dev</a></p>`
    }]
  };

  await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${sendgridKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(emailData)
  });

  return { statusCode: 200, body: JSON.stringify({ sent: true }) };
};
