// === HEADER NAVIGATION & MOBILE DRAWER ===

export function initNav() {
  const hamburgerBtn = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');
  const navHeader = document.querySelector('.nav-header');
  let lastFocusedElement = null;

  const closeMenu = () => {
    if (!hamburgerBtn || !mobileNav) return;
    mobileNav.classList.remove('open');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    if (lastFocusedElement === hamburgerBtn) {
      hamburgerBtn.focus();
    }
  };

  const openMenu = () => {
    if (!hamburgerBtn || !mobileNav) return;
    mobileNav.classList.add('open');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    const firstLink = mobileNav.querySelector('a');
    if (firstLink) firstLink.focus();
  };

  if (hamburgerBtn && mobileNav) {
    if (!mobileNav.id) {
      mobileNav.id = 'mobileNav';
    }
    hamburgerBtn.setAttribute('aria-controls', mobileNav.id);

    hamburgerBtn.addEventListener('click', () => {
      lastFocusedElement = document.activeElement;
      const isOpen = mobileNav.classList.contains('open');
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        closeMenu();
      });
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && mobileNav.classList.contains('open')) {
        closeMenu();
      }
    });
  }

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
