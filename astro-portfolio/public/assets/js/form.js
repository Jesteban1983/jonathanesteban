// === CONTACT FORM PREFILL & UTILITIES ===

export function initContactForm() {
  const form = document.getElementById('contactForm');
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
}
