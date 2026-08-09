// === CONTACT FORM VALIDATION, PREFILL & SERVERLESS SUBMISSION ===

export function initContactForm() {
  const form = document.getElementById('contactForm');
  const successBox = document.getElementById('formSuccess');

  if (!form) return;

  const subjectInput = form.querySelector('#subject');
  const messageInput = form.querySelector('#message');

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

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;

    // Check Honeypot
    const gotcha = form.querySelector('input[name="_gotcha"]');
    if (gotcha && gotcha.value !== '') {
      // Bot detected, silently ignore
      form.reset();
      return;
    }

    submitBtn.innerHTML = `⌛ Enviando mensaje...`;
    submitBtn.disabled = true;

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch('/api/contact-submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        form.style.display = 'none';
        if (successBox) {
          successBox.style.display = 'block';
        } else {
          window.location.href = '/gracias/';
        }
      } else {
        throw new Error('Error al procesar la solicitud');
      }
    } catch (error) {
      console.error('Contact Form Error:', error);
      submitBtn.innerHTML = `⚠️ Error al enviar — Inténtalo de nuevo`;
      submitBtn.disabled = false;
      setTimeout(() => {
        submitBtn.innerHTML = originalBtnText;
      }, 4000);
    }
  });
}
