// === THEME TOGGLE & PERSISTENCE (DARK/LIGHT) ===

export function initTheme() {
  const root = document.documentElement;
  const toggleButtons = document.querySelectorAll('[data-theme-toggle]');
  
  function updateAriaLabels(theme) {
    toggleButtons.forEach(btn => {
      btn.setAttribute('aria-label', `Cambiar a modo ${theme === 'dark' ? 'claro' : 'oscuro'}`);
    });
  }

  // Obtenemos el tema ya aplicado inmediatamente por el script en <head>
  const currentTheme = root.getAttribute('data-theme') || localStorage.getItem('site-theme') || 'light';
  updateAriaLabels(currentTheme);

  toggleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const active = root.getAttribute('data-theme');
      const nextTheme = active === 'dark' ? 'light' : 'dark';
      
      // Habilitar transiciones suaves solo durante el clic deliberado del usuario
      root.classList.add('theme-transitioning');
      root.setAttribute('data-theme', nextTheme);
      try {
        localStorage.setItem('site-theme', nextTheme);
      } catch (_) {}
      updateAriaLabels(nextTheme);

      setTimeout(() => {
        root.classList.remove('theme-transitioning');
      }, 300);
    });
  });
}
