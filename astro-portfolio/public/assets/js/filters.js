// === DYNAMIC PROJECT PORTFOLIO FILTERS ===

export function initProjectFilters() {
  const filterBtns = document.querySelectorAll('[data-filter]');
  const projectCards = document.querySelectorAll('[data-project-category]');

  if (filterBtns.length === 0 || projectCards.length === 0) return;

  const activeBtnClasses = [
    'bg-cyan-500',
    'text-white',
    'border-cyan-500'
  ];

  const inactiveBtnClasses = [
    'bg-slate-900/70',
    'text-slate-300',
    'border-slate-700'
  ];

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active', ...activeBtnClasses);
        b.classList.add(...inactiveBtnClasses);
        b.setAttribute('data-state', 'inactive');
      });

      btn.classList.add('active', ...activeBtnClasses);
      btn.classList.remove(...inactiveBtnClasses);
      btn.setAttribute('data-state', 'active');

      const filter = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = (card.getAttribute('data-project-category') || '')
          .split(',')
          .map((item) => item.trim())
          .filter(Boolean);
        if (filter === 'all' || category.includes(filter)) {
          card.hidden = false;
          card.removeAttribute('aria-hidden');
          card.classList.add('fade-in');
          setTimeout(() => card.classList.add('visible'), 50);
        } else {
          card.hidden = true;
          card.setAttribute('aria-hidden', 'true');
          card.classList.remove('visible');
        }
      });
    });
  });
}
