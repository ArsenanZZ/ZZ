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
        var palette = onDark ? ['#cdb7af', '#b4c9bd', '#b8c5d2', '#d0c2ac'] : ['#72534b', '#45675c', '#53677a', '#766044'];
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

    var bar = document.createElement('nav');
    bar.className = 'cn-copy-tools';
    var url = new URL(location.href); url.searchParams.set('wechat', '1');
    var link = document.createElement('a'); link.href = url.href; link.textContent = '公众号复制版';
    var button = document.createElement('button'); button.type = 'button'; button.textContent = '复制正文';
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
          properties.forEach(function (key) { target.style.setProperty(key, computed.getPropertyValue(key)); });
          target.style.setProperty('box-shadow','none'); target.style.setProperty('text-shadow','none'); target.style.setProperty('filter','none');
          if (node.tagName === 'IMG') { target.src = node.src; target.style.width = '100%'; target.style.height = 'auto'; target.removeAttribute('loading'); }
          if (node.tagName === 'A') target.href = node.href;
        });
        copy.querySelectorAll('script, style, .chapter-rail, button').forEach(function (node) { node.remove(); });
        output.append(copy);
      });
      return output;
    }
    button.addEventListener('click', async function () {
      button.disabled = true;
      try {
        var content = clipboardContent();
        if (navigator.clipboard && window.ClipboardItem) {
          await navigator.clipboard.write([new ClipboardItem({
            'text/html': new Blob([content.outerHTML], {type:'text/html'}),
            'text/plain': new Blob([content.textContent], {type:'text/plain'})
          })]);
        } else {
          var holder = document.createElement('div'); holder.style.cssText = 'position:fixed;left:-10000px;top:0;width:677px;'; holder.append(content); document.body.append(holder);
          var selection = getSelection(), previous = selection.rangeCount ? selection.getRangeAt(0).cloneRange() : null;
          var range = document.createRange(); range.selectNodeContents(content); selection.removeAllRanges(); selection.addRange(range);
          var copied = document.execCommand('copy'); holder.remove(); selection.removeAllRanges(); if (previous) selection.addRange(previous);
          if (!copied) throw new Error('Clipboard unavailable');
        }
        status.textContent = '已复制正文，可粘贴到公众号';
      } catch (error) { status.textContent = '未能自动复制，请在复制版中手动选择正文'; }
      finally { button.disabled = false; }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
