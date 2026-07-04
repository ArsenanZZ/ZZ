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
    var pieces = text.split(/[，。！？；：,.!?;:]/).map(function (s) { return s.trim(); }).filter(Boolean);
    for (var i = 0; i < pieces.length; i += 1) {
      var piece = pieces[i].replace(/^[-—\s]+/, '');
      if (/^[A-Za-z0-9\s.'-]+$/.test(piece)) continue;
      if (piece.length >= 6) return piece.slice(0, Math.min(16, piece.length));
    }
    return '';
  }

  function addAutoEmphasis() {
    var accents = ['accent-0', 'accent-1', 'accent-2', 'accent-3', 'accent-4'];
    var paragraphs = Array.prototype.slice.call(document.querySelectorAll('p[style*="text-align: justify"]'));
    var added = 0;
    paragraphs.forEach(function (p, index) {
      if (added >= 12) return;
      if (index % 3 !== 1) return;
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
      if (/^[A-Za-z0-9\s,.'’!?():@|·-]+$/.test(text) && /[A-Za-z]{3}/.test(text)) {
        p.innerHTML = '<em class="auto-english">' + escapeHtml(text) + '</em>';
      }
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
    addAutoEmphasis();
    italicizeEnglishNotes();
  });
})();
