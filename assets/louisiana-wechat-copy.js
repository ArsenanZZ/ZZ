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
  const imageMode = document.createElement('select');
  imageMode.setAttribute('aria-label', '图片复制方式');
  imageMode.style.cssText = scope.style.cssText;
  imageMode.add(new Option('带图片复制（原方式）', 'embedded'));
  imageMode.add(new Option('图片链接（备用）', 'links'));
  button.before(imageMode);
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
  const canonical = 'https://zhennanzhang.com/run50/wechat/louisiana-marathon-editorial.html';
  async function buildClipboard() {
    // Parse the saved document, not extension-modified live DOM.
    const response = await fetch(location.pathname, {cache: 'no-cache'});
    if (!response.ok) throw new Error('Article unavailable');
    const clean = new DOMParser().parseFromString(await response.text(), 'text/html');
    const source = clean.querySelector('main[data-edition]');
    const parts = [...source.children];
    const boundaries = [0, ...parts.flatMap((el, i) => el.classList.contains('chapter') || el.classList.contains('ending') ? [i] : [])];
    const selected = scope.value === 'all' ? parts : parts.slice(boundaries[Number(scope.value)], boundaries[Number(scope.value) + 1] ?? parts.length);
    const dark = document.documentElement.dataset.theme === 'dark';
    const theme = dark ? 'dark' : 'light';
    const ink = dark ? '#ece9e2' : '#262626';
    const muted = dark ? '#aaaaaa' : '#888888';
    const base = 'https://zhennanzhang.com/assets/louisiana-wechat-copy/';
    const wrapper = document.createElement('section');
    wrapper.style.cssText = `padding:0 4px 16px;background-color:${dark ? '#191919' : '#ffffff'};color:${ink};font-size:15px;line-height:1.95;text-align:left;font-family:Arial,"Microsoft YaHei",sans-serif;`;
    function convert(node) {
      if (node.nodeType === Node.TEXT_NODE) return document.createTextNode(node.textContent);
      if (node.nodeType !== Node.ELEMENT_NODE) return document.createTextNode('');
      const tag = node.tagName.toLowerCase();
      if (node.classList.contains('masthead') || node.classList.contains('byline')) return document.createTextNode('');
      if (['script','style','source','button'].includes(tag)) return document.createTextNode('');
      const number = node.classList.contains('chapter-number');
      const down = node.classList.contains('down');
      if (tag === 'img' || number || down) {
        const img = document.createElement('img');
        let url;
        if (number || down) url = base + (number ? 'number-' + node.textContent.trim() + '-universal.png' : 'arrows-' + theme + '.png');
        else {
          url = new URL(node.getAttribute('src'), canonical).href;
          const photo = url.match(/\/(img-\d+|la-[\d-]+)\.webp/);
          if (photo) url = base + photo[1] + '.jpg';
          if (url.includes('wechat-run50-map-louisiana-23-editorial.')) url = base + 'map.jpg';
          if (url.includes('wechat-louisiana-poster.')) url = base + 'poster.jpg';
        }
        img.src = url;
        img.alt = number ? node.textContent.trim() : down ? '向下' : node.getAttribute('alt') || '';
        img.style.cssText = `display:block;width:100%;max-width:100%;height:auto;margin:${down ? '24px 0 30px' : '0'};border:0;`;
        if (node.closest('.brand-intro')) {
          img.width = 96;
          img.height = 129;
          img.style.cssText = 'display:inline-block;width:96px;max-width:96px;height:auto;margin:0;border:0;vertical-align:middle;';
        }
        return img;
      }
      const inline = ['strong','b','em','i','u','span','a'].includes(tag);
      const outputTag = tag === 'h2' && node.closest('.ending') ? 'p' : ['p','br','strong','b','em','i','u','span','a','h1','h2'].includes(tag) ? tag : tag === 'figcaption' ? 'p' : 'section';
      const out = document.createElement(outputTag);
      if (inline) {
        if (tag === 'strong' || tag === 'b') out.style.fontWeight = '700';
        if (tag === 'em' || tag === 'i') out.style.fontStyle = 'italic';
        if (tag === 'u') out.style.textDecoration = 'underline';
        if (tag === 'a' && node.hasAttribute('href')) out.href = new URL(node.getAttribute('href'), canonical).href;
      } else if (tag !== 'br') {
        out.style.cssText = 'margin:0;padding:0;font-size:15px;line-height:1.95;text-align:left;';
        if (tag === 'p') out.style.marginBottom = '22px';
        if (node.classList.contains('prose') || node.closest('.intro')) out.style.textAlign = 'justify';
        if (tag === 'h1') out.style.cssText = 'margin:0 0 18px;font-size:25px;line-height:1.6;text-align:center;font-weight:700;';
        if (tag === 'h2') out.style.cssText = 'margin:0;font-size:20px;line-height:1.65;text-align:left;font-weight:700;';
        if (tag === 'figure') out.style.margin = '32px 0 36px';
        if (node.classList.contains('cover')) out.style.margin = '0 0 24px';
        if (tag === 'figcaption' || node.classList.contains('byline') || node.classList.contains('credits')) out.style.cssText = `margin:10px 0 22px;font-size:12px;line-height:1.9;text-align:center;color:${muted};`;
        if (node.classList.contains('chapter')) out.style.margin = '58px 0 34px';
        if (node.classList.contains('chapter-label')) out.style.cssText = `margin:18px 0 10px;font-size:11px;line-height:1.8;text-align:left;color:${muted};`;
        if (node.classList.contains('intro')) out.style.marginBottom = '54px';
        if (node.classList.contains('brand-intro')) out.style.cssText = 'margin:0 0 4px;padding:0;font-size:12px;line-height:1.5;text-align:center;';
        if (node.classList.contains('ending')) out.style.cssText = 'margin:64px 0 0;padding:32px 0 0;border-top:1px solid #888;font-size:14px;line-height:1.95;text-align:center;';
        if (node.closest('.ending')) {
          out.style.textAlign = 'center';
          out.setAttribute('align', 'center');
          if (tag === 'h2') out.style.cssText = 'margin:0;padding:0;font-size:24px;line-height:1.65;text-align:center;font-weight:700;';
          if (node.classList.contains('closing')) out.style.cssText = 'margin:0;padding:24px 0 0;font-size:13px;line-height:1.9;text-align:center;';
          if (node.classList.contains('credits')) out.style.marginTop = '36px';
        }
      }
      for (const child of node.childNodes) out.append(convert(child));
      return out;
    }
    for (const node of selected) wrapper.append(convert(node));
    if (imageMode.value === 'embedded') {
      const images = [...wrapper.querySelectorAll('img')];
      let next = 0;
      let completed = 0;
      await Promise.all(Array.from({length: 4}, async () => {
        while (next < images.length) {
          const img = images[next++];
          const url = new URL(img.src);
          const result = await fetch(url.pathname + url.search);
          if (!result.ok) throw new Error('Image unavailable');
          const blob = await result.blob();
          img.src = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
          status.textContent = `正在准备图片 ${++completed}/${images.length}…`;
        }
      }));
    }
    return wrapper;
  }

  async function copyArticle() {
    button.disabled = true;
    scope.disabled = imageMode.disabled = true;
    themeButtons.forEach(el => { el.disabled = true; });
    status.textContent = '正在复制…';
    try {
      const content = await buildClipboard();
      const html = content.outerHTML;
      const text = content.textContent;
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
      scope.disabled = imageMode.disabled = false;
      themeButtons.forEach(el => { el.disabled = false; });
    }
  }
  button.addEventListener('click', copyArticle);
})();
