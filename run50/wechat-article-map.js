(function () {
  var usCodeToIds = {
    AK: ['Alaska_1_'], AL: ['Alabama', 'alabama'], AR: ['Arkansas', 'Arkansas_1_'], AZ: ['Arizona', 'Arizona_1_'],
    CA: ['California'], CO: ['Colorado', 'Colorado_1_'], FL: ['Florida_1_'], GA: ['Georgia', 'Georgia_1_'],
    HI: ['Hawaii_1_', 'hawaii_1_'], IL: ['Illinois', 'Illinois_1_'], IN: ['Indiana', 'Indiana_1_'],
    KS: ['Kansas', 'Kansas_1_'], KY: ['Kentucky', 'Kentucky_1_'], LA: ['Louisiana_1_'],
    MI: ['Michigan', 'Michigan_1_'], MO: ['Missouri', 'Mossouri'], NC: ['North_Carolina_1_'],
    ND: ['North_Dakota', 'North_Dakota_1_'], NH: ['New_Hampshire', 'New_Hampshire_1_'],
    NY: ['New_York', 'New_York_2_'], OH: ['Ohio', 'Ohio_1_'], PA: ['Pensilvania', 'Pensilvania_1_'],
    SC: ['South_Carolina', 'South_Carolina_1_'], TN: ['Tennessee'], TX: ['Texas_1_'],
    VA: ['Virginia', 'Virginia_1_'], VT: ['Vermont', 'Vermont_1_'], WI: ['Wisconsin', 'Wisconsin_1_'],
    WV: ['West_Virginia', 'West_Virginia_1_']
  };

  function addSvgEl(svg, tag, attrs) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.keys(attrs || {}).forEach(function (key) { el.setAttribute(key, attrs[key]); });
    svg.appendChild(el);
    return el;
  }

  function unionBox(elements) {
    var box = null;
    elements.forEach(function (el) {
      var b;
      try { b = el.getBBox(); } catch (error) { return; }
      if (!box) {
        box = { x: b.x, y: b.y, x2: b.x + b.width, y2: b.y + b.height };
      } else {
        box.x = Math.min(box.x, b.x);
        box.y = Math.min(box.y, b.y);
        box.x2 = Math.max(box.x2, b.x + b.width);
        box.y2 = Math.max(box.y2, b.y + b.height);
      }
    });
    return box;
  }

  function markSvg(svg, elements, label) {
    elements.forEach(function (el) { el.classList.add('article-map-highlight'); });
    var box = unionBox(elements);
    if (!box) return;
    var cx = (box.x + box.x2) / 2;
    var cy = (box.y + box.y2) / 2;
    addSvgEl(svg, 'circle', { class: 'article-map-marker', cx: cx, cy: cy, r: 10 });
    var text = addSvgEl(svg, 'text', { class: 'article-map-label', x: cx + 16, y: cy - 14 });
    text.textContent = label;
  }

  function renderUs(slot) {
    if (typeof US_MAP_SVG === 'undefined') return false;
    slot.innerHTML = US_MAP_SVG;
    var svg = slot.querySelector('svg');
    if (!svg) return false;
    var code = (slot.dataset.region || '').toUpperCase();
    var ids = usCodeToIds[code] || [];
    var elements = ids.map(function (id) { return svg.querySelector('#map_' + id); }).filter(Boolean);
    if (elements.length) markSvg(svg, elements, code);
    return true;
  }

  function renderChina(slot) {
    if (typeof CHINA_MAP_SVG === 'undefined') return false;
    slot.innerHTML = CHINA_MAP_SVG;
    var svg = slot.querySelector('svg');
    if (!svg) return false;
    var id = slot.dataset.region || '';
    var el = svg.querySelector('#' + id);
    if (el) markSvg(svg, [el], slot.dataset.shortLabel || id.replace(/^cn_/, '').toUpperCase());
    return true;
  }

  function renderWorld(slot) {
    slot.innerHTML = '<div class="article-map-world"><b>RunWorld Map</b><span>' + (slot.dataset.label || '世界路线') + '</span></div>';
    return true;
  }

  function renderSlot(slot) {
    var kind = slot.dataset.mapKind;
    if (kind === 'us') return renderUs(slot);
    if (kind === 'china') return renderChina(slot);
    return renderWorld(slot);
  }

  document.addEventListener('DOMContentLoaded', function () {
    Array.prototype.forEach.call(document.querySelectorAll('.article-map-window[data-map-kind]'), renderSlot);
  });
})();
