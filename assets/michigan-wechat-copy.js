/* Page-specific rich-text export. No changes to other article pages. */
(() => {
  'use strict';
  const button = document.getElementById('copy-wechat');
  const status = document.getElementById('copy-status');
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

  function buildClipboard() {
    const source = document.querySelector('main[data-edition]');
    const copy = source.cloneNode(true);
    const originals = [source, ...source.querySelectorAll('*')];
    const copies = [copy, ...copy.querySelectorAll('*')];
    originals.forEach((node, i) => {
      const target = copies[i];
      const style = getComputedStyle(node);
      target.removeAttribute('style');
      properties.forEach(name => target.style.setProperty(name, style.getPropertyValue(name)));
      if (node.classList.contains('chapter-number')) {
        // WeChat may remove text-stroke: keep chapter numerals readable without it.
        target.style.color = document.documentElement.dataset.theme === 'dark' ? '#aaaaaa' : '#777777';
        target.style.fontSize = '72px';
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
    copy.querySelectorAll('script,style,source,button').forEach(el => el.remove());
    copy.querySelectorAll('img').forEach(img => {
      // Always use the public URLs, even when copying from a local preview.
      img.src = new URL(img.getAttribute('src'), canonical).href;
      img.removeAttribute('srcset');
      ['loading', 'decoding', 'fetchpriority', 'width', 'height'].forEach(a => img.removeAttribute(a));
      img.style.cssText = 'display:block;width:100%;max-width:100%;height:auto;margin:0 auto;border:0;';
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
      const content = buildClipboard();
      const html = content.outerHTML;
      const text = content.innerText || content.textContent;
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
      status.textContent = '已复制，请到公众号正文编辑区粘贴';
    } catch (_) {
      status.textContent = '复制未成功，请允许剪贴板权限后重试';
    } finally {
      button.disabled = false;
    }
  }
  button.addEventListener('click', copyArticle);
})();
