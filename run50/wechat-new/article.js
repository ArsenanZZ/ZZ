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
  const update = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (progress) progress.style.width = `${max > 0 ? Math.min(100,scrollY / max * 100) : 0}%`;
  };
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update);
  update();
})();
