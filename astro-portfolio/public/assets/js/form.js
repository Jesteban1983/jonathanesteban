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

    // Priority 1: Service from URL param (from service cards)
    const serviceFromUrl = params.get('service');
    if (serviceInput && serviceFromUrl) {
      serviceInput.value = serviceFromUrl;
    }

    // Priority 2: Subject-only URL param
    if (urlSubject) {
      if (subjectInput) subjectInput.value = urlSubject;
    }
    if (urlMessage) {
      if (messageInput) messageInput.value = urlMessage;
    }
  }

  applyPrefill();
}
