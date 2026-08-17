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
      // Don't close the whole mobile menu when clicking a dropdown TOGGLE
      // (the link that sits directly inside .nav-item-dropdown and has a .dropdown-menu sibling)
      const isToggle = link.parentElement?.classList.contains('nav-item-dropdown')
                    && link.nextElementSibling?.classList.contains('dropdown-menu');
      if (link.closest('.nav-mobile') && isToggle) return;
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

  // Desktop dropdown toggle for touch devices (tablets)
  // Prevents navigation and toggles dropdown via class on touch
  document.querySelectorAll('.nav-links .nav-item-dropdown > a').forEach(toggle => {
    toggle.addEventListener('click', function (e) {
      // Only intercept on touch-capable devices (not real mouse clicks)
      if ('ontouchstart' in window) {
        const parent = this.parentElement;
        const alreadyOpen = parent.classList.contains('dropdown-touch-open');
        if (alreadyOpen) {
          // Second tap → let the link navigate normally
          parent.classList.remove('dropdown-touch-open');
          return;
        }
        e.preventDefault();
        // Close any other open desktop dropdowns
        document.querySelectorAll('.nav-links .nav-item-dropdown.dropdown-touch-open').forEach(el => {
          if (el !== parent) el.classList.remove('dropdown-touch-open');
        });
        parent.classList.add('dropdown-touch-open');
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
