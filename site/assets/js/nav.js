// === HEADER NAVIGATION & MOBILE DRAWER ===

export function initNav() {
  const hamburgerBtn = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');
  const navHeader = document.querySelector('.nav-header');

  if (hamburgerBtn && mobileNav) {
    hamburgerBtn.addEventListener('click', () => {
      const isOpen = mobileNav.classList.toggle('open');
      hamburgerBtn.setAttribute('aria-expanded', String(isOpen));
    });

    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Mobile dropdown toggle
  document.querySelectorAll('.nav-mobile .nav-item-dropdown > a').forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      const parent = toggle.parentElement;
      const menu = parent.querySelector('.dropdown-menu');
      if (menu) {
        const isOpen = menu.classList.toggle('open');
        toggle.setAttribute('aria-expanded', String(isOpen));
      }
    });
  });

  // Active Link Highlighting based on current location
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a, .nav-mobile a');

  navLinks.forEach(link => {
    const linkPath = link.getAttribute('href');
    if (linkPath && (currentPath === linkPath || (linkPath !== '/' && currentPath.startsWith(linkPath)))) {
      link.classList.add('active');
    }
  });

  // Scroll Header Effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      navHeader?.classList.add('scrolled');
    } else {
      navHeader?.classList.remove('scrolled');
    }
  }, { passive: true });
}
