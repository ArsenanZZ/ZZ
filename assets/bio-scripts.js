document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu toggle
  const toggleBtn = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      navLinks.classList.toggle('show');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (navLinks.classList.contains('show') && !navLinks.contains(e.target) && e.target !== toggleBtn) {
        navLinks.classList.remove('show');
      }
    });
  }

  // Active link highlighting based on current URL path
  const path = window.location.pathname;
  const links = document.querySelectorAll('.nav-link');
  let matched = false;

  links.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;

    // Normalize paths to check matches
    const cleanHref = href.replace('../', '').replace('./', '');
    
    if (cleanHref && cleanHref.length > 0 && path.includes(cleanHref)) {
      link.classList.add('active');
      matched = true;
    }
  });

  // If no subpages matched, highlight the Home tab
  if (!matched) {
    links.forEach(link => {
      const href = link.getAttribute('href');
      if (href === '../' || href === './' || href === 'index.html' || href === './index.html') {
        link.classList.add('active');
      }
    });
  }
});
