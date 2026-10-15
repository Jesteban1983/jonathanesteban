// === PRIVACY-RESPECTING EVENT TRACKING & CONVERSION METRICS ===

export function initTracking() {
  // Track button clicks on CTAs
  document.querySelectorAll('[data-track-cta]').forEach(btn => {
    btn.addEventListener('click', () => {
      const label = btn.getAttribute('data-track-cta') || 'CTA Click';
      if (window.gtag) {
        window.gtag('event', 'conversion_click', { 'event_category': 'CTA', 'event_label': label });
      }
    });
  });
}
