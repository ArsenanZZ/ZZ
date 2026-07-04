(function () {
  var key = 'run50-wechat-article-theme';
  var root = document.documentElement;
  var button;

  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function (ch) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch];
    });
  }

  function updateButton() {
    if (!button) return;
    var isLight = root.dataset.theme === 'light';
    button.textContent = isLight ? 'Dark' : 'Light';
    button.setAttribute('aria-pressed', isLight ? 'true' : 'false');
  }

  function choosePhrase(text) {
    var pieces = text.split(/[\u3002\uff0c\uff01\uff1f\uff1b\uff1a,.!?;:]/).map(function (s) { return s.trim(); }).filter(Boolean);
    for (var i = 0; i < pieces.length; i += 1) {
      var piece = pieces[i].replace(/^[-\u2014\s]+/, '');
      if (/^[A-Za-z0-9\s.'-]+$/.test(piece)) continue;
      if (piece.length >= 6) return piece.slice(0, Math.min(16, piece.length));
    }
    return '';
  }

  function colorizeExistingStrong() {
    var accents = ['accent-0', 'accent-1', 'accent-2', 'accent-3', 'accent-4'];
    Array.prototype.forEach.call(document.querySelectorAll('strong'), function (strong, index) {
      if (!strong.classList.contains('auto-emphasis')) strong.classList.add('auto-emphasis');
      if (!Array.prototype.some.call(strong.classList, function (name) { return /^accent-\d$/.test(name); })) {
        strong.classList.add(accents[index % accents.length]);
      }
    });
  }

  function addAutoEmphasis() {
    var accents = ['accent-0', 'accent-1', 'accent-2', 'accent-3', 'accent-4'];
    var paragraphs = Array.prototype.slice.call(document.querySelectorAll('p[style*="text-align: justify"]'));
    var added = 0;
    paragraphs.forEach(function (p, index) {
      if (added >= 24) return;
      if (index % 2 !== 1) return;
      if (p.querySelector('strong, em, .auto-emphasis')) return;
      if (Array.prototype.some.call(p.childNodes, function (node) { return node.nodeType !== 3; })) return;
      var text = p.textContent.trim();
      if (text.length < 44) return;
      var phrase = choosePhrase(text);
      if (!phrase) return;
      var start = text.indexOf(phrase);
      if (start < 0) return;
      var before = text.slice(0, start);
      var after = text.slice(start + phrase.length);
      p.innerHTML = escapeHtml(before) + '<strong class="auto-emphasis ' + accents[added % accents.length] + '">' + escapeHtml(phrase) + '</strong>' + escapeHtml(after);
      added += 1;
    });
  }

  function italicizeEnglishNotes() {
    Array.prototype.forEach.call(document.querySelectorAll('p'), function (p) {
      var text = p.textContent.trim();
      if (!text || p.querySelector('em, strong, .auto-english')) return;
      if (/^[A-Za-z0-9\s,.'\u2019!?():@|\u00b7-]+$/.test(text) && /[A-Za-z]{3}/.test(text)) {
        p.innerHTML = '<em class="auto-english">' + escapeHtml(text) + '</em>';
      }
    });
  }

  function captionFromAlt(alt) {
    var text = (alt || '').replace(/\s+/g, ' ').trim();
    if (!text) return '跑马现场记录';
    text = text.replace(/奖牌封面/g, '奖牌质感封面');
    text = text.replace(/故事照片\s*(\d+)/g, '现场照片 $1');
    if (text.length > 36) text = text.slice(0, 36) + '...';
    return text;
  }

  function addMissingCaptions() {
    Array.prototype.forEach.call(document.querySelectorAll('section img'), function (img) {
      if (img.closest('.wechat-vlog-panel')) return;
      var next = img.nextElementSibling;
      if (next && next.tagName === 'P' && next.textContent.trim()) return;
      var caption = document.createElement('p');
      caption.className = 'auto-caption';
      caption.textContent = captionFromAlt(img.getAttribute('alt'));
      img.insertAdjacentElement('afterend', caption);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    button = document.querySelector('.article-theme-toggle');
    updateButton();
    if (button) {
      button.addEventListener('click', function () {
        var next = root.dataset.theme === 'light' ? 'dark' : 'light';
        root.dataset.theme = next;
        try { localStorage.setItem(key, next); } catch (error) {}
        updateButton();
      });
    }
    colorizeExistingStrong();
    addAutoEmphasis();
    italicizeEnglishNotes();
    addMissingCaptions();
  });
})();
