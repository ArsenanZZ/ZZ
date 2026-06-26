/* zz-wechat.js — "一键排版" floating toolbar for WeChat copy */
(function () {
  'use strict';

  var article = document.querySelector('main article');
  if (!article) return;

  /* ── Floating toolbar ── */
  var toolbar = document.createElement('div');
  toolbar.id = 'zz-wechat-toolbar';
  toolbar.style.cssText = 'position:fixed;bottom:20px;right:20px;display:flex;flex-direction:column;gap:8px;z-index:9000;';

  var btn = document.createElement('button');
  btn.id = 'zz-btn-layout';
  btn.textContent = '⊞ 一键排版';
  btn.style.cssText = [
    'background:#ffffff;border:1px solid #d0dfe8;border-radius:8px;',
    'padding:8px 14px;cursor:pointer;font-size:13px;font-weight:800;',
    'color:#344252;box-shadow:0 2px 8px rgba(0,0,0,.10);',
    'white-space:nowrap;font-family:inherit;line-height:1;'
  ].join('');

  toolbar.appendChild(btn);
  document.body.appendChild(toolbar);
  btn.addEventListener('click', doFormat);

  /* ── Main: build WeChat HTML and copy/preview ── */
  function doFormat() {
    var baseUrl = window.location.protocol + '//' + window.location.host +
      window.location.pathname.replace(/\/[^/]+$/, '/');

    var clone = article.cloneNode(true);
    applyInlineStyles(clone, baseUrl);
    var html = wrapForPreview(clone.innerHTML);

    if (navigator.clipboard && window.ClipboardItem) {
      var blob = new Blob([html], { type: 'text/html' });
      navigator.clipboard.write([new ClipboardItem({ 'text/html': blob })])
        .then(function () { flash('✓ 已复制，去公众号 Ctrl+V 粘贴', true); })
        .catch(function () { openPreview(html); });
    } else {
      openPreview(html);
    }
  }

  /* ── Apply WeChat-native inline styles ── */
  function applyInlineStyles(el, baseUrl) {

    /* H2: section-label → centered divider; regular → bold with # prefix */
    el.querySelectorAll('h2').forEach(function (h2) {
      var isLabel = h2.classList.contains('section-label');
      var text = h2.textContent.trim();

      if (isLabel) {
        h2.setAttribute('style',
          'text-align:center;font-size:14px;font-weight:400;color:#cccccc;' +
          'letter-spacing:.15em;margin:24px 0 14px;padding:0;');
        h2.textContent = '———— · ' + text + ' · ————';
      } else {
        h2.setAttribute('style',
          'font-size:18px;font-weight:bold;color:#1a1a1a;' +
          'line-height:1.4;margin:20px 0 10px;padding:0;');
        h2.innerHTML = '';
        var mark = document.createElement('span');
        mark.setAttribute('style', 'color:#0b67c2;margin-right:4px;');
        mark.textContent = '#';
        h2.appendChild(mark);
        h2.appendChild(document.createTextNode(text));
      }
    });

    /* Paragraphs */
    el.querySelectorAll('p').forEach(function (p) {
      if (p.classList.contains('end-mark') || p.classList.contains('credit-line')) {
        p.setAttribute('style',
          'text-align:center;color:#999999;font-size:13px;margin:3px 0;padding:0;');
      } else if (p.classList.contains('place')) {
        p.setAttribute('style',
          'font-size:14px;color:#4a6fa5;font-weight:bold;' +
          'background:#eef3fa;border-radius:4px;padding:5px 10px;margin:0 0 12px;');
      } else {
        p.setAttribute('style',
          'font-size:16px;line-height:1.8;color:#3d3d3d;margin:0 0 14px;padding:0;');
      }
    });

    /* Figures */
    el.querySelectorAll('figure').forEach(function (fig) {
      fig.setAttribute('style', 'margin:14px 0;padding:0;');
    });

    /* Images — convert relative src to absolute */
    el.querySelectorAll('figure img').forEach(function (img) {
      var src = img.getAttribute('src') || '';
      if (src && !src.startsWith('http') && !src.startsWith('//')) {
        img.setAttribute('src', baseUrl + src);
      }
      img.setAttribute('style', 'width:100%;max-width:100%;height:auto;display:block;');
      img.removeAttribute('loading');
      img.removeAttribute('decoding');
    });

    /* Captions */
    el.querySelectorAll('figcaption, .caption-line').forEach(function (cap) {
      cap.setAttribute('style',
        'font-size:12px;color:#999999;text-align:center;margin-top:4px;line-height:1.5;padding:0;');
    });
  }

  /* ── Wrap in a WeChat-safe, self-contained preview page ── */
  function wrapForPreview(inner) {
    return [
      '<!DOCTYPE html><html><head>',
      '<meta charset="utf-8">',
      '<meta name="viewport" content="width=device-width,initial-scale=1">',
      '<title>公众号预览</title>',
      '<style>',
      'body{margin:0;padding:20px 0;background:#f0f0f0;}',
      '.wc{max-width:660px;margin:0 auto;background:#fff;padding:24px 20px;}',
      '.tip{max-width:660px;margin:12px auto;text-align:center;color:#888;font-size:13px;font-family:sans-serif;}',
      '</style>',
      '</head><body>',
      '<div class="wc">' + inner + '</div>',
      '<p class="tip">全选 (Ctrl+A) → 复制 (Ctrl+C) → 粘贴到公众号编辑器</p>',
      '</body></html>'
    ].join('');
  }

  function openPreview(html) {
    var win = window.open('', '_blank', 'width=740,height=860,scrollbars=yes');
    if (win) {
      win.document.open();
      win.document.write(html);
      win.document.close();
    } else {
      flash('请允许弹出窗口后重试', false);
    }
  }

  function flash(msg, ok) {
    var b = document.getElementById('zz-btn-layout');
    var orig = b.textContent;
    b.textContent = msg;
    b.style.background = ok ? '#ecfdf5' : '#fef2f2';
    b.style.color = ok ? '#065f46' : '#991b1b';
    setTimeout(function () {
      b.textContent = orig;
      b.style.background = '#ffffff';
      b.style.color = '#344252';
    }, 3000);
  }
}());
