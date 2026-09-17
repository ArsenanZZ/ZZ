(function () {
  'use strict';
  function ready() {
    var root = document.documentElement;
    var forCopy = new URLSearchParams(location.search).get('wechat') === '1';
    root.dataset.cnCopy = String(forCopy);
    if (forCopy) root.dataset.theme = 'light';
    else if (root.dataset.theme !== 'light' && root.dataset.theme !== 'dark') root.dataset.theme = 'dark';
    var containers = Array.from(document.querySelectorAll('[data-cn-content]'));
    var nodes = containers.flatMap(function (node) { return [node].concat(Array.from(node.querySelectorAll('*'))); });
    var originals = new WeakMap();
    nodes.forEach(function (node) { originals.set(node, node.getAttribute('style')); });
    function isDarkBackground(node) {
      for (var current = node; current && current !== document.body; current = current.parentElement) {
        var style = getComputedStyle(current);
        var rgb = style.backgroundColor.match(/[\d.]+/g);
        if (rgb && (rgb.length < 4 || Number(rgb[3]) > 0.5)) {
          return Number(rgb[0]) * .2126 + Number(rgb[1]) * .7152 + Number(rgb[2]) * .0722 < 145;
        }
        if (style.backgroundImage !== 'none') return true;
      }
      return false;
    }
    function synchronize() {
      nodes.forEach(function (node) {
        var style = originals.get(node);
        if (style === null) node.removeAttribute('style'); else node.setAttribute('style', style);
      });
      var dark = root.dataset.theme === 'dark';
      var colors = nodes.map(function (node) { return dark || isDarkBackground(node) ? '#ffffff' : '#333333'; });
      var backgrounds = nodes.map(function (node) { return getComputedStyle(node).backgroundColor; });
      nodes.forEach(function (node, index) {
        node.style.setProperty('color', colors[index], 'important');
        node.style.setProperty('box-shadow', 'none', 'important');
        node.style.setProperty('text-shadow', 'none', 'important');
        node.style.setProperty('filter', 'none', 'important');
        if (dark && backgrounds[index] !== 'rgba(0, 0, 0, 0)' && backgrounds[index] !== 'transparent') {
          node.style.setProperty('background-color', '#242424', 'important');
        }
      });
      containers.forEach(function (node) { node.style.setProperty('background-color', dark ? '#181818' : '#ffffff', 'important'); });
      nodes.forEach(function (node) {
        var kind = node.getAttribute('data-cn-emphasis');
        if (!kind) return;
        var onDark = dark || isDarkBackground(node.parentElement);
        var tone = Number(node.getAttribute('data-cn-tone') || 0) % 4;
        var palette = onDark ? ['#e6a397', '#91cfab', '#9cc7ed', '#e3c183'] : ['#ac4336', '#237953', '#306eaa', '#9a681c'];
        var color = palette[tone];
        node.style.setProperty('font-weight', '800', 'important');
        node.style.setProperty('display', 'inline', 'important');
        node.style.removeProperty('background');
        node.style.setProperty('background-image', 'none', 'important');
        node.style.setProperty('background-color', 'transparent', 'important');
        node.style.setProperty('border', '0', 'important');
        node.style.setProperty('padding', '0', 'important');
        node.style.setProperty('box-decoration-break', 'clone');
        node.style.setProperty('-webkit-box-decoration-break', 'clone');
        if (kind === 'underline') {
          node.style.setProperty('border-bottom', '3px solid ' + color, 'important');
          node.style.setProperty('padding-bottom', '2px', 'important');
        }
        node.style.setProperty('color', color, 'important');
        node.querySelectorAll('*').forEach(function (child) { child.style.setProperty('color', color, 'important'); });
      });
      document.querySelectorAll('.cn-end-title').forEach(function (node) {
        node.style.setProperty('color', dark ? '#f4ba55' : '#b66b0d', 'important');
      });
      var oldToggle = document.querySelector('.article-theme-toggle');
      if (oldToggle) { oldToggle.textContent = dark ? 'Light' : 'Dark'; oldToggle.setAttribute('aria-pressed', String(!dark)); }
      var newToggle = document.querySelector('.theme-toggle');
      if (newToggle) newToggle.textContent = dark ? '浅色' : '深色';
    }
    synchronize();
    new MutationObserver(synchronize).observe(root, { attributes: true, attributeFilter: ['data-theme'] });

    var oneClick = document.body.dataset.cnOneClick === 'true';
    var bar = document.createElement('nav');
    bar.className = 'cn-copy-tools';
    var url = new URL(location.href); url.searchParams.set('wechat', '1');
    var link = document.createElement('a'); link.href = url.href; link.textContent = '公众号复制版';
    var button = document.createElement('button'); button.type = 'button'; button.textContent = oneClick ? '一键复制到公众号' : '复制正文';
    var status = document.createElement('span'); status.className = 'cn-copy-status'; status.setAttribute('role', 'status');
    bar.append(link, button, status); document.body.append(bar);
    var properties = ['color','background-color','background-image','font-family','font-size','font-weight','font-style','line-height','letter-spacing','text-align','text-decoration','display','padding-top','padding-right','padding-bottom','padding-left','margin-top','margin-right','margin-bottom','margin-left','border-left','border-right','border-top','border-bottom','border-radius','box-sizing','box-decoration-break','-webkit-box-decoration-break','position','top','right','bottom','left','overflow','aspect-ratio'];
    function clipboardContent() {
      var output = document.createElement('section');
      containers.forEach(function (source) {
        var copy = source.cloneNode(true);
        var from = [source].concat(Array.from(source.querySelectorAll('*')));
        var to = [copy].concat(Array.from(copy.querySelectorAll('*')));
        from.forEach(function (node, index) {
          var target = to[index], computed = getComputedStyle(node);
          properties.forEach(function (key) {
            // Keep authored layout units: computed auto margins become desktop-sized
            // pixel offsets, and percentage padding must adapt to the paste target.
            var layout = /^(margin-|padding-|top$|right$|bottom$|left$)/.test(key);
            var authored = node.style.getPropertyValue(key);
            target.style.setProperty(key, layout && authored ? authored : computed.getPropertyValue(key));
          });
          target.style.setProperty('box-shadow','none'); target.style.setProperty('text-shadow','none'); target.style.setProperty('filter','none');
          if (node.tagName === 'SECTION' || node.tagName === 'IMG') {
            target.style.setProperty('box-sizing', 'border-box');
            target.style.setProperty('max-width', '100%');
          }
          if (node.tagName === 'IMG') { target.src = node.src; target.style.width = '100%'; target.style.height = 'auto'; target.removeAttribute('loading'); }
          if (node.tagName === 'A') target.href = node.href;
        });
        copy.querySelectorAll('script, style, .chapter-rail, button').forEach(function (node) { node.remove(); });
        // Turn ratio-based text posters into normal flow for narrow rich-text editors.
        copy.querySelectorAll('section').forEach(function (frame) {
          var panel = frame.firstElementChild;
          if (!/%$/.test(frame.style.paddingTop) || !panel || panel.style.position !== 'absolute') return;
          frame.style.paddingTop = '0';
          frame.style.height = 'auto';
          panel.style.position = 'static';
          panel.style.inset = 'auto';
          panel.querySelectorAll('section').forEach(function (item) {
            if (item.style.position !== 'absolute') return;
            // Decorative play icon has no video action in the copied article.
            if (item.querySelector('span') && item.style.borderRadius === '50%') { item.remove(); return; }
            item.style.position = 'static';
            item.style.inset = 'auto';
            item.style.marginTop = '16px';
          });
        });
        // The editor supplies the page width and outer spacing.
        copy.style.setProperty('width', '100%');
        copy.style.setProperty('max-width', '100%');
        copy.style.setProperty('min-width', '0');
        copy.style.setProperty('margin', '0');
        copy.style.setProperty('padding', '0');
        copy.style.setProperty('box-sizing', 'border-box');
        output.append(copy);
      });
      return output;
    }
    button.addEventListener('click', async function () {
      button.disabled = true;
      try {
        var themeBeforeCopy = root.dataset.theme;
        var content;
        try {
          if (oneClick) { root.dataset.theme = 'light'; synchronize(); }
          content = clipboardContent();
        } finally {
          if (oneClick) { root.dataset.theme = themeBeforeCopy; synchronize(); }
        }
        function legacyCopy() {
          var holder = document.createElement('div'); holder.style.cssText = 'position:fixed;left:-10000px;top:0;width:677px;'; holder.append(content); document.body.append(holder);
          var selection = getSelection(), previous = selection.rangeCount ? selection.getRangeAt(0).cloneRange() : null;
          try {
            var range = document.createRange(); range.selectNodeContents(content); selection.removeAllRanges(); selection.addRange(range);
            if (!document.execCommand('copy')) throw new Error('Clipboard unavailable');
          } finally {
            holder.remove(); selection.removeAllRanges(); if (previous) selection.addRange(previous);
          }
        }
        if (navigator.clipboard && window.ClipboardItem) {
          try {
            await navigator.clipboard.write([new ClipboardItem({
              'text/html': new Blob([content.outerHTML], {type:'text/html'}),
              'text/plain': new Blob([content.textContent], {type:'text/plain'})
            })]);
          } catch (error) { legacyCopy(); }
        } else { legacyCopy(); }
        status.textContent = oneClick ? '已复制图文，请到公众号编辑器粘贴' : '已复制正文，可粘贴到公众号';
      } catch (error) { status.textContent = '未能自动复制，请在复制版中手动选择正文'; }
      finally { button.disabled = false; }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
