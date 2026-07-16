(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');
  try {
    const saved = localStorage.getItem('run50-wechat-theme');
    if (saved === 'light') root.dataset.theme = 'light';
  } catch (error) {}

  const syncToggle = () => {
    if (toggle) toggle.textContent = root.dataset.theme === 'light' ? '深色' : '浅色';
  };
  syncToggle();
  toggle?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    try { localStorage.setItem('run50-wechat-theme', root.dataset.theme); } catch (error) {}
    syncToggle();
  });

  const progress = document.querySelector('.reading-progress');
  const railLinks = Array.from(document.querySelectorAll('.chapter-rail a[href^="#"]'));
  const chapterTargets = railLinks.map((link) => {
    const id = decodeURIComponent(link.getAttribute('href').slice(1));
    return { link, section: document.getElementById(id) };
  }).filter((item) => item.section);

  const syncChapter = () => {
    if (!chapterTargets.length) return;
    const marker = scrollY + Math.min(innerHeight * .3, 240);
    let current = chapterTargets[0];
    chapterTargets.forEach((item) => {
      if (item.section.offsetTop <= marker) current = item;
    });
    chapterTargets.forEach((item) => {
      const active = item === current;
      item.link.classList.toggle('is-active', active);
      if (active) item.link.setAttribute('aria-current', 'location');
      else item.link.removeAttribute('aria-current');
    });
  };

  const update = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (progress) progress.style.width = `${max > 0 ? Math.min(100,scrollY / max * 100) : 0}%`;
    syncChapter();
  };
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update);
  update();
})();
