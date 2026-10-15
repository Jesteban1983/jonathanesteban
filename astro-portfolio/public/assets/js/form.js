// === CONTACT FORM VALIDATION, PREFILL & SERVERLESS SUBMISSION ===

export function initContactForm() {
  const form = document.getElementById('contactForm');
  const successBox = document.getElementById('formSuccess');
  const errorBox = document.getElementById('formError');

  if (!form) return;

  const subjectInput = form.querySelector('#subject');
  const messageInput = form.querySelector('#message');
  const serviceInput = form.querySelector('#service');

  function applyPrefill() {
    const params = new URLSearchParams(window.location.search);
    const isBudgetPrefill = params.get('prefill') === 'budget';
    const urlSubject = params.get('subject');
    const urlMessage = params.get('message');

    // Priority 1: URL params from calculator ("Solicitar Esta Propuesta")
    if (isBudgetPrefill && (urlSubject || urlMessage)) {
      if (subjectInput && urlSubject) subjectInput.value = urlSubject;
      if (messageInput && urlMessage) messageInput.value = urlMessage;
      localStorage.removeItem('budgetPrefill');
      return;
    }

    const serviceFromUrl = params.get('service');
    if (serviceInput && serviceFromUrl) {
      serviceInput.value = serviceFromUrl;
    }

    // Priority 2: Subject-only URL param (from service card "Consultar →")
    if (urlSubject && !isBudgetPrefill) {
      if (subjectInput) subjectInput.value = urlSubject;
      return;
    }

    // No URL params → direct visit → clear stale localStorage → form stays blank
    localStorage.removeItem('budgetPrefill');
  }

  applyPrefill();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (errorBox) {
      errorBox.style.display = 'none';
      errorBox.textContent = '';
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;

    // Check Honeypot
    const gotcha = form.querySelector('input[name="company_site"]');
    if (gotcha && gotcha.value !== '') {
      // Bot detected, silently ignore
      form.reset();
      return;
    }

    if (!form.checkValidity()) {
      form.reportValidity();
      const firstInvalid = form.querySelector(':invalid');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    const messageValue = messageInput?.value || '';
    if (messageValue.length > 2000) {
      if (errorBox) {
        errorBox.textContent = 'El mensaje supera el límite de 2000 caracteres.';
        errorBox.style.display = 'block';
      }
      messageInput?.focus();
      return;
    }

    submitBtn.innerHTML = `⌛ Enviando mensaje...`;
    submitBtn.disabled = true;

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.consentReply = form.querySelector('#consentReply')?.checked === true;
    data.consentWhatsapp = form.querySelector('#consentWhatsapp')?.checked === true;
    data.sourcePath = window.location.pathname;

    try {
      const response = await fetch('/api/contact-submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        // Redirigir a la página de gracias
        window.location.href = '/gracias/?email=' + encodeURIComponent(data.email);
      } else {
        // Try to parse error, fall back to generic message
        let errorMsg = 'Error al procesar la solicitud';
        try {
          const serverError = await response.json();
          errorMsg = serverError.error || errorMsg;
        } catch (_) {
          errorMsg = response.status === 429
            ? 'Demasiadas solicitudes. Espera unos minutos e inténtalo de nuevo.'
            : 'Error del servidor (' + response.status + '). Inténtalo de nuevo.';
        }
        throw new Error(errorMsg);
      }
    } catch (error) {
      console.error('Contact Form Error:', error);
      if (errorBox) {
        errorBox.textContent = error.message || 'Error al enviar. Inténtalo de nuevo.';
        errorBox.style.display = 'block';
      }
      submitBtn.innerHTML = `⚠️ Error al enviar — Inténtalo de nuevo`;
      submitBtn.disabled = false;
      setTimeout(() => {
        submitBtn.innerHTML = originalBtnText;
      }, 4000);
    }
  });
}
