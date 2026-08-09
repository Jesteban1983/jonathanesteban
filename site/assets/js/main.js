// === BOOTSTRAP & MAIN INITIALIZATION MODULE ===

import { initTheme } from './theme.js';
import { initNav } from './nav.js';
import { initFAQ } from './faq.js';
import { initProjectFilters } from './filters.js';
import { initContactForm } from './form.js';
import { initCalculator } from './calculator.js';
import { initTracking } from './tracking.js';
import { initDemoApp } from './app-demo.js';

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNav();
  initFAQ();
  initProjectFilters();
  initContactForm();
  initCalculator();
  initTracking();
  initDemoApp();

  // Scroll Animations Observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
});
