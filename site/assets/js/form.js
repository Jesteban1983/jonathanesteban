// === CONTACT FORM VALIDATION, PREFILL & SERVERLESS SUBMISSION ===

export function initContactForm() {
  const form = document.getElementById('contactForm');
  const successBox = document.getElementById('formSuccess');

  if (!form) return;

  const subjectInput = form.querySelector('#subject');
  const messageInput = form.querySelector('#message');

  function applyBudgetPrefill() {
    const params = new URLSearchParams(window.location.search);
    const isBudgetPrefill = params.get('prefill') === 'budget';
    const urlSubject = params.get('subject');
    const urlMessage = params.get('message');

    let prefill = null;

    if (isBudgetPrefill && (urlSubject || urlMessage)) {
      prefill = {
        subject: urlSubject || '',
        message: urlMessage || ''
      };
    } else {
      const savedPrefill = localStorage.getItem('budgetPrefill');
      if (savedPrefill) {
        try {
          prefill = JSON.parse(savedPrefill);
        } catch {
          prefill = null;
        }
      }
    }

    if (!prefill) return;

    if (subjectInput && !subjectInput.value.trim()) {
      subjectInput.value = prefill.subject || '';
    }

    if (messageInput && !messageInput.value.trim()) {
      messageInput.value = prefill.message || '';
    }

    localStorage.removeItem('budgetPrefill');
  }

  applyBudgetPrefill();

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
