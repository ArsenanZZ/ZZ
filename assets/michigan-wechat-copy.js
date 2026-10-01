/* Page-specific rich-text export. No changes to other article pages. */
(() => {
  'use strict';
  const button = document.getElementById('copy-wechat');
  const status = document.getElementById('copy-status');
  const article = document.querySelector('main[data-edition]');
  const children = [...article.children];
  const starts = [0, ...children.flatMap((el, i) => el.classList.contains('chapter') || el.classList.contains('ending') ? [i] : [])];
  const scope = document.createElement('select');
  scope.setAttribute('aria-label', '选择全文或分段复制');
  scope.style.cssText = 'max-width:180px;padding:9px 6px;font-size:13px;color:inherit;background:transparent;border:1px solid #888;border-radius:4px;';
  scope.add(new Option('全文复制', 'all'));
  starts.forEach((start, i) => scope.add(new Option(i === 0 ? '分段：开篇' : children[start].classList.contains('ending') ? '分段：结尾和署名' : `分段：第 ${i} 章`, String(i))));
  button.before(scope);
  function selectedChildren() {
    if (scope.value === 'all') return children;
    const i = Number(scope.value);
    return children.slice(starts[i], starts[i + 1] ?? children.length);
  }
  const themeButtons = document.querySelectorAll('[data-theme-choice]');
  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    themeButtons.forEach(el => el.setAttribute('aria-pressed', String(el.dataset.themeChoice === theme)));
    status.textContent = '';
  }
  themeButtons.forEach(el => el.addEventListener('click', () => setTheme(el.dataset.themeChoice)));
  const canonical = 'https://zhennanzhang.com/run50/wechat/michigan-meadows-marathon-modern-rail.html';
  const properties = ['display', 'box-sizing', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
    'padding-top', 'padding-right', 'padding-bottom', 'padding-left', 'font-family', 'font-size',
    'font-weight', 'font-style', 'line-height', 'letter-spacing', 'text-align', 'text-decoration',
    'color', 'background-color', 'border-top', 'border-right', 'border-bottom', 'border-left',
    'border-radius', 'white-space', 'overflow-wrap'];

  async function buildClipboard() {
    const source = document.querySelector('main[data-edition]');
    const copy = source.cloneNode(true);
    const originals = [source, ...source.querySelectorAll('*')];
    const copies = [copy, ...copy.querySelectorAll('*')];
    const ornaments = [];
    originals.forEach((node, i) => {
      const target = copies[i];
      const style = getComputedStyle(node);
      target.removeAttribute('style');
      properties.forEach(name => target.style.setProperty(name, style.getPropertyValue(name)));
      if (['STRONG', 'B', 'EM', 'I', 'U', 'A', 'SPAN'].includes(node.tagName) && style.display === 'inline') {
        // Keep inline emphasis minimal; block-layout properties can split text on paste.
        target.removeAttribute('style');
        ['font-weight', 'font-style', 'text-decoration', 'color'].forEach(name =>
          target.style.setProperty(name, style.getPropertyValue(name)));
      }
      if (node.classList.contains('chapter-number') || node.classList.contains('down')) {
        ornaments.push({node, target});
      }
      if (node.classList.contains('brand-intro')) {
        target.style.width = '280px';
        target.style.maxWidth = '100%';
        target.style.margin = '0 auto 12px';
      }
      target.removeAttribute('class');
      target.removeAttribute('id');
      [...target.attributes].filter(a => a.name.startsWith('data-') || a.name.startsWith('on'))
        .forEach(a => target.removeAttribute(a.name));
    });
    const chosen = new Set(selectedChildren());
    [...copy.children].forEach((el, i) => { if (!chosen.has(children[i])) el.remove(); });
    copy.querySelectorAll('script,style,source,button').forEach(el => el.remove());
    copy.querySelectorAll('img').forEach(img => {
      // Always use the public URLs, even when copying from a local preview.
      img.src = new URL(img.getAttribute('src'), canonical).href;
      img.removeAttribute('srcset');
      ['loading', 'decoding', 'fetchpriority', 'width', 'height'].forEach(a => img.removeAttribute(a));
      img.style.cssText = 'display:block;width:100%;max-width:100%;height:auto;margin:0 auto;border:0;';
    });
    const images = [...copy.querySelectorAll('img')];
    let done = 0;
    async function embedImage(img) {
      // Read from this page's origin: local previews must not depend on deployment.
      const url = new URL(img.src);
      const response = await fetch(url.pathname + url.search);
      if (!response.ok) throw new Error('Image unavailable');
      let blob = await response.blob();
      if (!/\.gif$/i.test(url.pathname)) {
        const bitmap = await createImageBitmap(blob);
        const canvas = document.createElement('canvas');
        const scale = Math.min(1, 800 / bitmap.width);
        canvas.width = Math.round(bitmap.width * scale);
        canvas.height = Math.round(bitmap.height * scale);
        const context = canvas.getContext('2d');
        context.fillStyle = '#fff';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
        bitmap.close();
        blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.72));
      }
      img.src = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
      status.textContent = `正在准备图片 ${++done}/${images.length}…`;
    }
    // Limit decoding concurrency so long articles also work on smaller devices.
    let next = 0;
    await Promise.all(Array.from({length: 4}, async () => {
      while (next < images.length) await embedImage(images[next++]);
    }));
    // Rasterize only ornaments: WeChat strips text-stroke and may reset alignment.
    // Full-width transparent strips preserve both the outlines and arrow position.
    ornaments.forEach(({node, target}) => {
      const number = node.classList.contains('chapter-number');
      const style = getComputedStyle(node);
      const width = Math.round(node.getBoundingClientRect().width);
      const size = parseFloat(style.fontSize);
      const height = number ? Math.ceil(size) : 48;
      const canvas = document.createElement('canvas');
      canvas.width = width * 2;
      canvas.height = height * 2;
      const context = canvas.getContext('2d');
      context.scale(2, 2);
      context.strokeStyle = number ? getComputedStyle(document.body).color : '#aaaaaa';
      context.lineWidth = number ? 1 : 1.5;
      if (number) {
        context.font = `${style.fontWeight} ${size}px ${style.fontFamily}`;
        context.textBaseline = 'alphabetic';
        let x = 1;
        for (const char of node.textContent.trim()) {
          context.strokeText(char, x, size * 0.81);
          x += context.measureText(char).width + parseFloat(style.letterSpacing || 0);
        }
      } else {
        for (const y of [7, 20, 33]) {
          context.beginPath();
          context.moveTo(width / 2 - 5, y);
          context.lineTo(width / 2, y + 6);
          context.lineTo(width / 2 + 5, y);
          context.stroke();
        }
      }
      const img = document.createElement('img');
      img.src = canvas.toDataURL('image/png');
      img.alt = number ? node.textContent.trim() : '向下';
      img.width = width;
      img.height = height;
      img.style.cssText = `display:block;width:100%;max-width:100%;height:auto;border:0;margin:${number ? '0' : '24px 0 30px'};`;
      target.replaceWith(img);
    });
    copy.querySelectorAll('a[href]').forEach(a => { a.href = new URL(a.getAttribute('href'), canonical).href; });
    // Use editor-friendly section/p tags while retaining the inlined visual styles.
    [...copy.querySelectorAll('header,footer,figure,figcaption,picture')].forEach(el => {
      const replacement = document.createElement(el.tagName === 'FIGCAPTION' ? 'p' : 'section');
      [...el.attributes].forEach(a => replacement.setAttribute(a.name, a.value));
      replacement.append(...el.childNodes);
      el.replaceWith(replacement);
    });
    const wrapper = document.createElement('section');
    wrapper.style.cssText = 'width:100%;max-width:677px;margin:0 auto;padding:0;box-sizing:border-box;background:#ffffff;color:#262626;font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif;';
    const palette = getComputedStyle(document.body);
    wrapper.style.backgroundColor = palette.backgroundColor;
    wrapper.style.color = palette.color;
    wrapper.style.padding = '16px';
    wrapper.append(...copy.childNodes);
    return wrapper;
  }

  async function copyArticle() {
    button.disabled = true;
    status.textContent = '正在复制…';
    try {
      const content = await buildClipboard();
      const html = content.outerHTML;
      const text = selectedChildren().map(el => el.innerText || el.textContent).join('\n\n');
      let copied = false;
      if (navigator.clipboard && window.ClipboardItem) {
        try {
          await navigator.clipboard.write([new ClipboardItem({
            'text/html': new Blob([html], {type:'text/html'}),
            'text/plain': new Blob([text], {type:'text/plain'})
          })]);
          copied = true;
        } catch (_) { /* Older browsers can still copy through a selection. */ }
      }
      if (!copied) {
        const holder = document.createElement('div');
        holder.style.cssText = 'position:fixed;left:-10000px;top:0;width:677px;background:white;';
        holder.append(content);
        document.body.append(holder);
        const selection = window.getSelection();
        const previous = selection.rangeCount ? selection.getRangeAt(0).cloneRange() : null;
        const writeRichText = event => {
          if (event.clipboardData) {
            event.clipboardData.setData('text/html', html);
            event.clipboardData.setData('text/plain', text);
            event.preventDefault();
          }
        };
        document.addEventListener('copy', writeRichText);
        try {
          const range = document.createRange();
          range.selectNodeContents(content);
          selection.removeAllRanges();
          selection.addRange(range);
          if (!document.execCommand('copy')) throw new Error('Copy unavailable');
        } finally {
          document.removeEventListener('copy', writeRichText);
          holder.remove();
          selection.removeAllRanges();
          if (previous) selection.addRange(previous);
        }
      }
      status.textContent = scope.value === 'all' ? '已复制；如公众号截断，请选择分段复制' : '本段已复制，请按顺序粘贴到公众号';
    } catch (_) {
      status.textContent = '复制未成功，请允许剪贴板权限后重试';
    } finally {
      button.disabled = false;
    }
  }
  button.addEventListener('click', copyArticle);
})();
