// === INTERACTIVE FAQ SEARCH & ACCORDION ===

export function initFAQ() {
  const faqAccordion = document.getElementById('faqAccordion');
  const faqSearchInput = document.getElementById('faqSearchInput');
  const categoryFilters = document.querySelectorAll('[data-faq-category]');

  if (!faqAccordion) return;

  // Toggle Accordion Items
  faqAccordion.addEventListener('click', (e) => {
    const questionBtn = e.target.closest('.faq-question');
    if (!questionBtn) return;

    const faqItem = questionBtn.closest('.faq-item');
    const isActive = faqItem.classList.contains('active');

    // Close all items
    faqAccordion.querySelectorAll('.faq-item').forEach(item => {
      item.classList.remove('active');
    });

    // Toggle clicked item
    if (!isActive) {
      faqItem.classList.add('active');
    }
  });

  // Search Filter
  if (faqSearchInput) {
    faqSearchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase().trim();
      const items = faqAccordion.querySelectorAll('.faq-item');

      items.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(term)) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  // Category Filter
  if (categoryFilters.length > 0) {
    categoryFilters.forEach(btn => {
      btn.addEventListener('click', () => {
        categoryFilters.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const cat = btn.getAttribute('data-faq-category');
        const items = faqAccordion.querySelectorAll('.faq-item');

        items.forEach(item => {
          const itemCat = item.getAttribute('data-category');
          if (cat === 'all' || itemCat === cat) {
            item.style.display = 'block';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }
}
