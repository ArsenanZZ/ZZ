(function () {
  var US_PATHS = {
    IL: ['Illinois', 'Kentucky_1_'], TN: ['Alabama'], WV: ['West_Virginia', 'Virginia_1_'],
    TX: ['Kansas_1_'], FL: ['South_Carolina_1_'], NC: ['Maryland'], AR: ['Tennessee', 'Arkansas'],
    SC: ['South_Carolina', 'Indiana_1_'], KY: ['Georgia_1_', 'Kentucky'], PA: ['Pensilvania', 'New_Jersey_1_'],
    WI: ['Wisconsin', 'Illinois_1_'], MI: ['Michigan', 'Ocean'], NH: ['New_Hampshire', 'Maine_1_'],
    LA: ['Arkansas_1_'], VA: ['North_Carolina_1_', 'Virginia'], ND: ['South_Dakota_1_', 'North_Dakota'],
    KS: ['Kansas', 'North_Dakota_1_'], VT: ['New_Hampshire_1_', 'Vermont'], AL: ['alabama', 'Missispi'],
    AZ: ['Arizona_1_', 'Utah'], DE: ['Massachusets_1_'], MN: ['Minnesotta', 'Wisconsin_1_'],
    CT: ['New_York_2_', 'Connecticut'], RI: ['Delaware', 'Rhode_Island'], MA: ['Vermont_1_', 'Massachusets'],
    ME: ['Michigan_1_', 'Maine'], OH: ['Ohio', 'West_Virginia_1_'], NY: ['Rhode_Island_1_', 'New_York'],
    CA: ['Arizona'], IN: ['Indiana', 'Ohio_1_'], HI: ['ocean_2_'], GA: ['Georgia', 'Florida_1_'],
    CO: ['Texas_1_', 'Colorado'], AK: ['ocean_3_'], MO: ['Iowa_1_', 'Missouri']
  };

  var US_SOURCE_PATHS = [
    'Illinois', 'Alabama', 'West_Virginia', 'Kansas_1_', 'South_Carolina_1_', 'Maryland',
    'Tennessee', 'South_Carolina', 'Georgia_1_', 'Pensilvania', 'Wisconsin', 'Michigan',
    'Ocean', 'Vermont', 'New_Hampshire', 'Arkansas_1_', 'North_Carolina_1_',
    'South_Dakota_1_', 'Kansas', 'New_Hampshire_1_', 'alabama', 'Arizona_1_',
    'Massachusets_1_', 'Minnesotta', 'New_York_2_', 'Connecticut', 'Vermont_1_',
    'Michigan_1_', 'Ohio', 'New_York', 'Arizona', 'Indiana', 'Georgia', 'Texas_1_',
    'Iowa_1_', 'Idaho', 'Minessota', 'Mossouri', 'Washington_1_', 'Nebraska',
    'Nevada_41_', 'New_Jersey', 'Idaho_1_', 'Oklahoma', 'Nevada_1_', 'South_Dakota',
    'Utah_1_', 'Montana_1_', 'Pensilvania_1_', 'ocean_2_', 'Oklahoma_1_', 'ocean_3_',
    'Kentucky', 'Arkansas', 'North_Dakota', 'North_Dakota_1_', 'Colorado', 'Montana',
    'Wyoming_1_', 'New_Mexico_1_', 'New_Mexico', 'Oregon_41_', 'West_Virginia_1_',
    'Ohio_1_', 'Indiana_1_', 'Florida_1_', 'Kentucky_1_', 'Colorado_1_', 'Maine',
    'Maine_1_', 'New_Jersey_1_', 'Iowa', 'Missouri', 'Missisppi', 'Missispi',
    'Louisiana_1_', 'Utah', 'California', 'Connecticut_1_', 'Nebraska_1_',
    'Illinois_1_', 'Massachusets', 'Wisconsin_1_', 'Wyoming', 'Oregon_1_', 'Virginia',
    'Virginia_1_', 'Rhode_Island_1_', 'Rhode_Island', 'Delaware'
  ];

  var US_HOLLOW_PATHS = [
    'South_Carolina_1_', 'Arizona', 'Michigan', 'Oklahoma_1_', 'Alabama', 'Maryland',
    'ocean_3_', 'Kansas_1_', 'Arkansas_1_', 'Illinois', 'West_Virginia',
    'South_Carolina', 'Pensilvania', 'Wisconsin', 'Vermont', 'New_Hampshire',
    'Kansas', 'alabama', 'Arizona_1_', 'Minnesotta', 'Ohio', 'New_York', 'Indiana',
    'Georgia', 'Alaska_1_', 'Idaho', 'Nebraska', 'Nevada_41_', 'Oklahoma',
    'South_Dakota', 'Utah_1_', 'Pensilvania_1_'
  ];

  var US_LABEL_PATHS = [
    'line_13_', 'NV', 'UT', 'ID', 'MT', 'ND', 'MN', 'IA', 'WI', 'IL', 'MO', 'AR', 'LA',
    'MS', 'AL', 'TN', 'KY', 'IN', 'MI', 'OH', 'WV', 'VA', 'SC', 'NC', 'PA',
    'NY', 'ME', 'GA', 'FL', 'SD', 'NE', 'KS', 'OK', 'WY', 'CO', 'OR', 'WA',
    'CA', 'HI', 'AZ', 'AK', 'NM', 'TX', 'VT_1_', 'NH_1_', 'MD', 'DE_1_',
    'NJ_1_', 'CT_1_', 'RI_1_', 'STATES', 'ATLANTIC_OCEAN', 'gulf_of_mexico',
    'OCEANS'
  ];

  var US_COLORS = {
    AK: '#d4614a', AL: '#98c038', AR: '#5ca860', AZ: '#e89838', CA: '#d4614a',
    CO: '#9068c0', CT: '#9068c0', DE: '#e89838', FL: '#d4614a', GA: '#e89838',
    HI: '#9068c0', IL: '#9068c0', IN: '#e89838', KS: '#3898a8', KY: '#98c038',
    LA: '#98c038', MA: '#3898a8', ME: '#d4614a', MI: '#3898a8', MN: '#e89838',
    MO: '#e89838', NC: '#98c038', ND: '#5ca860', NH: '#e89838', NY: '#e89838',
    OH: '#5ca860', PA: '#d4614a', RI: '#d4614a', SC: '#9068c0', TN: '#3898a8',
    TX: '#9068c0', VA: '#5ca860', VT: '#98c038', WI: '#5ca860', WV: '#e89838'
  };

  var US_CITY_BY_FILE = {
    'anchorage-marathon-modern-rail.html': ['AK', 'Anchorage', 61.2181, -149.9003],
    'arizona-phoenix-marathon-modern-rail.html': ['AZ', 'Buckeye', 33.3703, -112.5838],
    'atlanta-marathon-modern-rail.html': ['GA', 'Atlanta', 33.7490, -84.3880],
    'blue-ridge-marathon-modern-rail.html': ['VA', 'Roanoke', 37.2710, -79.9414],
    'chicago-marathon-modern-rail.html': ['IL', 'Chicago', 41.8781, -87.6298],
    'cincinnati-flying-pig-marathon-modern-rail.html': ['OH', 'Cincinnati', 39.1031, -84.5120],
    'cleveland-marathon-modern-rail.html': ['OH', 'Cleveland', 41.4993, -81.6944],
    'denver-colfax-marathon-modern-rail.html': ['CO', 'Denver', 39.7392, -104.9903],
    'disney-marathon-modern-rail.html': ['FL', 'Orlando', 28.5383, -81.3792],
    'fargo-marathon-modern-rail.html': ['ND', 'Fargo', 46.8772, -96.7898],
    'green-bay-marathon-modern-rail.html': ['WI', 'Green Bay', 44.5133, -88.0133],
    'hatfield-mccoy-marathon-modern-rail.html': ['KY', 'Williamson', 37.6743, -82.2774],
    'hell-on-gravel-marathon-modern-rail.html': ['KS', 'El Dorado', 37.8172, -96.8623],
    'honolulu-marathon-modern-rail.html': ['HI', 'Honolulu', 21.3069, -157.8583],
    'indianapolis-monumental-marathon-modern-rail.html': ['IN', 'Indianapolis', 39.7684, -86.1581],
    'kentucky-derby-marathon-2021-modern-rail.html': ['KY', 'Louisville', 38.2527, -85.7585],
    'kentucky-derby-marathon-2023-modern-rail.html': ['KY', 'Louisville', 38.2527, -85.7585],
    'kentucky-derby-marathon-2025-modern-rail.html': ['KY', 'Louisville', 38.2527, -85.7585],
    'kentucky-derby-marathon-modern-rail.html': ['KY', 'Louisville', 38.2527, -85.7585],
    'little-rock-marathon-modern-rail.html': ['AR', 'Little Rock', 34.7465, -92.2896],
    'louisiana-marathon-modern-rail.html': ['LA', 'Baton Rouge', 30.4515, -91.1871],
    'louisville-marathon-2024-modern-rail.html': ['KY', 'Louisville', 38.2527, -85.7585],
    'louisville-marathon-modern-rail.html': ['KY', 'Louisville', 38.2527, -85.7585],
    'mad-marathon-modern-rail.html': ['VT', 'Warren', 44.1206, -72.8512],
    'miami-marathon-modern-rail.html': ['FL', 'Miami', 25.7617, -80.1918],
    'michigan-meadows-marathon-modern-rail.html': ['MI', 'Grand Rapids', 42.9634, -85.6681],
    'nashville-marathon-modern-rail.html': ['TN', 'Nashville', 36.1627, -86.7816],
    'new-hampshire-clarence-demar-marathon-modern-rail.html': ['NH', 'Keene', 42.9337, -72.2781],
    'new-york-city-marathon-modern-rail.html': ['NY', 'New York City', 40.7128, -74.0060],
    'north-carolina-oak-island-marathon-modern-rail.html': ['NC', 'Oak Island', 33.9166, -78.1611],
    'pittsburgh-marathon-modern-rail.html': ['PA', 'Pittsburgh', 40.4406, -79.9959],
    'rocket-city-marathon-modern-rail.html': ['AL', 'Huntsville', 34.7304, -86.5861],
    'san-antonio-marathon-modern-rail.html': ['TX', 'San Antonio', 29.4241, -98.4936],
    'san-francisco-marathon-modern-rail.html': ['CA', 'San Francisco', 37.7749, -122.4194],
    'south-carolina-marathon-modern-rail.html': ['SC', 'Greer', 34.9387, -82.2271],
    'st-joseph-marathon-modern-rail.html': ['MO', 'St. Joseph', 39.7675, -94.8467],
    'west-virginia-marathon-modern-rail.html': ['WV', 'Huntington', 38.4192, -82.4452]
  };

  var SPECIAL_US_DOTS = {
    'AK:Anchorage': [275, 917],
    'HI:Honolulu': [570, 933],
    'VT:Warren': [1466, 270],
    'NH:Keene': [1502, 310]
  };

  var US_PROGRESS_EXPERIMENT = {
    KY: ['KY'],
    OH: ['KY', 'OH'],
    NY: ['KY', 'OH', 'NY']
  };

  var US_PROGRESS_CITY_DOTS = {
    KY: ['KY', 'Louisville', 38.2527, -85.7585],
    OH: ['OH', 'Cleveland', 41.4993, -81.6944],
    NY: ['NY', 'New York City', 40.7128, -74.0060]
  };

  function addSvgEl(parent, tag, attrs) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.keys(attrs || {}).forEach(function (key) { el.setAttribute(key, attrs[key]); });
    parent.appendChild(el);
    return el;
  }

  function unique(items) {
    return items.filter(function (item, index) { return items.indexOf(item) === index; });
  }

  function lightenHex(hex, amount) {
    var value = String(hex || '').replace('#', '');
    if (!/^[0-9a-f]{6}$/i.test(value)) return hex;
    return '#' + [0, 2, 4].map(function (index) {
      var channel = parseInt(value.slice(index, index + 2), 16);
      var next = Math.round(channel + (255 - channel) * amount);
      return next.toString(16).padStart(2, '0');
    }).join('');
  }

  function splitUsPath(d) {
    return (d.match(/[Mm][^Mm]*/g) || [d]).map(function (part) { return part.trim(); }).filter(Boolean);
  }

  function pathPartBox(part) {
    var pairs = part.match(/-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?/g) || [];
    if (!pairs.length) return { xMin: 0, xMax: 0, yMin: 0, yMax: 0, area: 0 };
    var xs = pairs.map(function (pair) { return parseFloat(pair); });
    var ys = pairs.map(function (pair) { return parseFloat(pair.split(',')[1]); });
    var xMin = Math.min.apply(Math, xs);
    var xMax = Math.max.apply(Math, xs);
    var yMin = Math.min.apply(Math, ys);
    var yMax = Math.max.apply(Math, ys);
    return { xMin: xMin, xMax: xMax, yMin: yMin, yMax: yMax, area: (xMax - xMin) * (yMax - yMin) };
  }

  function removeContainedPathParts(svg) {
    var cleanupIds = unique(US_SOURCE_PATHS.concat(US_HOLLOW_PATHS, Object.keys(US_PATHS).reduce(function (all, code) {
      return all.concat(US_PATHS[code]);
    }, [])));
    cleanupIds.forEach(function (stateId) {
      var el = svg.querySelector('#map_' + stateId);
      if (!el) return;
      var parts = splitUsPath(el.getAttribute('d') || '');
      if (parts.length < 2) return;
      var boxes = parts.map(pathPartBox);
      var maxArea = Math.max.apply(Math, boxes.map(function (box) { return box.area; }));
      if (!maxArea) return;
      el.removeAttribute('fill-rule');
      el.setAttribute('d', parts.filter(function (_, index) {
        var box = boxes[index];
        var isContained = isContainedPathBox(box, boxes, index);
        if (isAlaskaPanhandleGap(stateId, box) && isContained) return false;
        if (box.area < maxArea * 0.05) return true;
        return !isContained;
      }).join(' '));
    });
  }

  function projectUs(lat, lon) {
    var lat0 = 37.5 * Math.PI / 180;
    var lon0 = -96 * Math.PI / 180;
    var lat1 = 29.5 * Math.PI / 180;
    var lat2 = 45.5 * Math.PI / 180;
    var n = 0.5 * (Math.sin(lat1) + Math.sin(lat2));
    var c = Math.cos(lat1) * Math.cos(lat1) + 2 * n * Math.sin(lat1);
    var rho0 = Math.sqrt(c - 2 * n * Math.sin(lat0)) / n;
    var latRad = lat * Math.PI / 180;
    var lonRad = lon * Math.PI / 180;
    var theta = n * (lonRad - lon0);
    var rho = Math.sqrt(c - 2 * n * Math.sin(latRad)) / n;
    return {
      x: 1798.50 * rho * Math.sin(theta) + 935.11,
      y: -1851.29 * (rho0 - rho * Math.cos(theta)) + 579.07
    };
  }

  function projectCity(abbr, city, lat, lon) {
    var special = SPECIAL_US_DOTS[abbr + ':' + city];
    if (special) return { x: special[0], y: special[1] };
    return projectUs(lat, lon);
  }

  function usStateGroup(svg, code) {
    return (US_PATHS[code] || []).map(function (id) {
      return svg.querySelector('#map_' + id);
    }).filter(Boolean);
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

  function usPathBox(path) {
    return pathPartBox(path.getAttribute('d') || '');
  }

  function containsUsBox(outer, inner) {
    return outer.area > inner.area * 1.08 &&
      inner.xMin >= outer.xMin - 2 &&
      inner.xMax <= outer.xMax + 2 &&
      inner.yMin >= outer.yMin - 2 &&
      inner.yMax <= outer.yMax + 2;
  }

  function isContainedPathBox(box, boxes, index) {
    return boxes.some(function (outer, outerIndex) {
      return outerIndex !== index && containsUsBox(outer, box);
    });
  }

  function isAlaskaPanhandleGap(stateId, box) {
    return stateId === 'ocean_3_' && box.xMin > 340 && box.yMin > 950;
  }

  function visibleBoundaryPaths(paths) {
    var boxed = paths.map(function (path) { return { path: path, box: usPathBox(path) }; });
    return boxed
      .filter(function (item) { return item.box.area > 18; })
      .filter(function (item) {
        return !boxed.some(function (other) {
          return other.path !== item.path && containsUsBox(other.box, item.box);
        });
      })
      .map(function (item) { return item.path; });
  }

  function addBoundaryLayer(svg, statePaths, progressMode, mapTheme) {
    var lightMode = mapTheme === 'light';
    var layer = addSvgEl(svg, 'g', { class: 'article-map-state-boundaries' });
    layer.style.pointerEvents = 'none';
    visibleBoundaryPaths(statePaths).forEach(function (path) {
      var outline = path.cloneNode(false);
      outline.removeAttribute('id');
      outline.setAttribute('fill', 'none');
      outline.setAttribute('stroke', progressMode ? (lightMode ? 'rgba(18,24,31,.66)' : 'rgba(255,255,255,.58)') : 'rgba(31,41,55,.58)');
      outline.setAttribute('stroke-width', progressMode ? (lightMode ? '.64' : '1.05') : '1.05');
      outline.setAttribute('stroke-linejoin', 'round');
      outline.setAttribute('stroke-linecap', 'round');
      outline.setAttribute('vector-effect', 'non-scaling-stroke');
      if (progressMode && lightMode) outline.setAttribute('stroke-dasharray', '5 4');
      outline.style.opacity = progressMode ? (lightMode ? '.78' : '.86') : '1';
      outline.style.pointerEvents = 'none';
      layer.appendChild(outline);
    });
  }

  function addCurrentOutline(svg, elements, progressMode, mapTheme) {
    var lightMode = mapTheme === 'light';
    var layer = addSvgEl(svg, 'g', { class: 'article-map-current-layer' });
    layer.style.pointerEvents = 'none';
    visibleBoundaryPaths(elements).forEach(function (path) {
      var outline = path.cloneNode(false);
      outline.removeAttribute('id');
      outline.setAttribute('class', progressMode ? 'article-map-current-state article-map-progress-current-outline' : 'article-map-current-state');
      outline.setAttribute('fill', 'none');
      outline.setAttribute('stroke', progressMode ? (lightMode ? '#17202b' : '#ffd166') : '#10151f');
      outline.setAttribute('stroke-width', progressMode ? (lightMode ? '1.55' : '1.7') : '5.8');
      outline.setAttribute('stroke-linejoin', 'round');
      outline.setAttribute('stroke-linecap', 'round');
      outline.setAttribute('vector-effect', 'non-scaling-stroke');
      layer.appendChild(outline);
    });
  }

  function raiseLabels(svg, progressMode, mapTheme) {
    var lightMode = mapTheme === 'light';
    US_LABEL_PATHS.forEach(function (labelId) {
      var label = svg.querySelector('#map_' + labelId);
      if (!label) return;
      var ocean = labelId === 'ATLANTIC_OCEAN' || labelId === 'gulf_of_mexico' || labelId === 'OCEANS';
      var nevada = labelId === 'NV' || labelId === 'line_13_';
      var fill = ocean ? (progressMode ? (lightMode ? '#1f2a33' : '#9aa5b8') : '#526072') : (nevada ? (lightMode ? '#0f172a' : '#ffffff') : (progressMode ? (lightMode ? '#151a22' : '#f8fbff') : '#1f2937'));
      var stroke = ocean ? 'none' : (nevada ? (lightMode ? 'rgba(255,255,255,.92)' : 'rgba(2,6,23,.95)') : (progressMode ? (lightMode ? 'none' : 'rgba(255,255,255,.24)') : 'rgba(255,255,255,.48)'));
      var strokeWidth = ocean ? '0' : (nevada ? '2.4' : (progressMode ? (lightMode ? '0' : '.45') : '.65'));
      label.setAttribute('fill', fill);
      label.setAttribute('stroke', stroke);
      label.setAttribute('stroke-width', strokeWidth);
      label.setAttribute('paint-order', 'stroke fill');
      label.style.opacity = ocean ? (progressMode ? (lightMode ? '.72' : '.34') : '.42') : (nevada ? '1' : (progressMode ? (lightMode ? '1' : '.98') : '.92'));
      label.style.fill = fill;
      label.style.stroke = stroke;
      label.style.strokeWidth = strokeWidth;
      label.style.filter = nevada ? (lightMode ? 'drop-shadow(0 1px 1px rgba(255,255,255,.9))' : 'drop-shadow(0 1px 1px rgba(0,0,0,.7))') : '';
      label.style.pointerEvents = 'none';
      svg.appendChild(label);
    });
  }

  function restoreInsetLand(svg, mapTheme) {
    var lightMode = mapTheme === 'light';
    var fill = lightMode ? '#dedad3' : '#242b3f';
    var stroke = lightMode ? 'none' : 'none';
    ['map_outer_borders', 'map_hawaii_1_'].forEach(function (id) {
      var el = svg.querySelector('#' + id);
      if (!el) return;
      el.setAttribute('fill', fill);
      el.setAttribute('stroke', stroke);
      el.setAttribute('stroke-width', '0');
      el.style.opacity = '1';
      el.style.pointerEvents = 'none';
    });
  }

  function paintBaseMap(svg, progressCodes, mapTheme) {
    removeContainedPathParts(svg);
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    var progressMode = Array.isArray(progressCodes) && progressCodes.length > 0;
    var currentCode = progressMode ? progressCodes[progressCodes.length - 1] : '';
    var lightMode = mapTheme === 'light';

    var stateIds = unique(US_SOURCE_PATHS.concat(Object.keys(US_PATHS).reduce(function (all, code) {
      return all.concat(US_PATHS[code]);
    }, [])));
    var allStatePaths = [];

    Array.prototype.forEach.call(svg.querySelectorAll('path[id^="map_"]'), function (path) {
      var id = path.id.replace(/^map_/, '');
      var isState = stateIds.indexOf(id) >= 0;
      var isLabel = US_LABEL_PATHS.indexOf(id) >= 0;
      var isFrame = id === 'USA' || id === 'White' || id === 'exterior_2_' || id === 'Color' || id === 'States';

      if (isState) {
        var baseFill = progressMode ? (lightMode ? '#dedad3' : '#242b3f') : '#dedad3';
        path.classList.add('article-map-state-base');
        path.setAttribute('fill', baseFill);
        path.setAttribute('stroke', progressMode ? 'none' : 'rgba(31,41,55,.64)');
        path.setAttribute('stroke-width', progressMode ? '0' : '.9');
        path.setAttribute('stroke-linejoin', 'round');
        path.setAttribute('vector-effect', 'non-scaling-stroke');
        path.style.opacity = progressMode ? (lightMode ? '1' : '.78') : '1';
        path.style.pointerEvents = 'none';
        allStatePaths.push(path);
        return;
      }

      if (isLabel) {
        path.style.pointerEvents = 'none';
        return;
      }

      if (isFrame) {
        path.setAttribute('fill', progressMode ? (lightMode ? '#a9d8f0' : '#323a52') : '#a8d4e8');
        path.setAttribute('stroke', progressMode ? (lightMode ? (id === 'USA' ? 'none' : 'rgba(18,24,31,.28)') : 'rgba(207,218,232,.28)') : 'rgba(31,41,55,.35)');
        path.setAttribute('stroke-width', progressMode ? (lightMode ? (id === 'USA' ? '0' : '.52') : '.8') : '.6');
        path.style.opacity = '1';
        path.style.pointerEvents = 'none';
        return;
      }

      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', progressMode ? (lightMode ? 'rgba(18,24,31,.44)' : 'rgba(207,218,232,.18)') : 'rgba(31,41,55,.16)');
      path.setAttribute('stroke-width', progressMode ? (lightMode ? '.62' : '.55') : '.45');
      path.style.opacity = progressMode ? (lightMode ? '.5' : '.32') : '.18';
      path.style.pointerEvents = 'none';
    });

    if (progressMode) restoreInsetLand(svg, mapTheme);

    var coloredCodes = progressMode ? progressCodes : Object.keys(US_COLORS);
    coloredCodes.forEach(function (code) {
      usStateGroup(svg, code).forEach(function (path) {
        path.classList.add('article-map-run-state');
        if (progressMode) path.classList.add(code === currentCode ? 'article-map-progress-current' : 'article-map-progress-previous');
        var isCurrent = progressMode && code === currentCode;
        var runColor = isCurrent ? lightenHex(US_COLORS[code], 0.12) : US_COLORS[code];
        path.setAttribute('fill', runColor);
        path.style.fill = runColor;
        path.setAttribute('stroke', progressMode ? (isCurrent ? (lightMode ? 'rgba(255,255,255,.96)' : '#ffe08a') : 'none') : 'rgba(31,41,55,.72)');
        path.setAttribute('stroke-width', progressMode ? (isCurrent ? '1.35' : '0') : '1');
        path.setAttribute('stroke-linejoin', 'round');
        path.setAttribute('stroke-linecap', 'round');
        path.setAttribute('vector-effect', 'non-scaling-stroke');
        path.style.opacity = progressMode && code !== currentCode ? '1' : '1';
        path.style.filter = '';
      });
    });

    addBoundaryLayer(svg, allStatePaths, progressMode, mapTheme);
    return allStatePaths;
  }

  function currentFileName() {
    return (window.location.pathname.split('/').pop() || '').toLowerCase();
  }

  function addCityMarker(svg, slot, code, elements) {
    var race = US_CITY_BY_FILE[currentFileName()];
    var p;
    var label = slot.dataset.shortLabel || code;
    if (race) {
      p = projectCity(race[0], race[1], race[2], race[3]);
      label = race[0];
    } else {
      var box = unionBox(elements);
      if (!box) return;
      p = { x: (box.x + box.x2) / 2, y: (box.y + box.y2) / 2 };
    }

    var group = addSvgEl(svg, 'g', { class: 'article-map-city-marker' });
    addSvgEl(group, 'circle', { class: 'article-map-marker-glow', cx: p.x.toFixed(1), cy: p.y.toFixed(1), r: '22' });
    addSvgEl(group, 'circle', { class: 'article-map-marker-ring', cx: p.x.toFixed(1), cy: p.y.toFixed(1), r: '13' });
    addSvgEl(group, 'circle', { class: 'article-map-marker', cx: p.x.toFixed(1), cy: p.y.toFixed(1), r: '9' });
    var text = addSvgEl(group, 'text', { class: 'article-map-label', x: (p.x + 20).toFixed(1), y: (p.y - 14).toFixed(1) });
    text.textContent = label;
  }

  function addProgressCityDots(svg, progressCodes, currentCode, mapTheme) {
    var lightMode = mapTheme === 'light';
    var glowLayer = addSvgEl(svg, 'g', { class: 'article-map-progress-dot-glows' });
    var dotLayer = addSvgEl(svg, 'g', { class: 'article-map-progress-dots' });
    progressCodes.forEach(function (code) {
      var race = US_PROGRESS_CITY_DOTS[code];
      if (!race) return;
      var p = projectCity(race[0], race[1], race[2], race[3]);
      addSvgEl(glowLayer, 'circle', {
        class: 'article-map-progress-dot-glow',
        cx: p.x.toFixed(1),
        cy: p.y.toFixed(1),
        r: lightMode ? '18' : '20.2'
      });
      addSvgEl(dotLayer, 'circle', {
        class: code === currentCode ? 'article-map-progress-dot article-map-progress-dot-current' : 'article-map-progress-dot',
        cx: p.x.toFixed(1),
        cy: p.y.toFixed(1),
        r: lightMode ? '8.8' : '8.8'
      });
    });
  }

  function markChinaSvg(svg, elements, label) {
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
    var progressCodes = US_PROGRESS_EXPERIMENT[code] || null;
    var progressMode = !!progressCodes;
    var mapTheme = slot.dataset.mapTheme === 'light' ? 'light' : 'dark';
    if (progressMode) slot.classList.add('article-map-progress-experiment');
    slot.classList.add(mapTheme === 'light' ? 'article-map-force-light' : 'article-map-force-dark');
    paintBaseMap(svg, progressCodes, mapTheme);
    var elements = usStateGroup(svg, code);
    if (elements.length) {
      if (!progressMode) addCurrentOutline(svg, elements, progressMode, mapTheme);
      if (progressMode) {
        addProgressCityDots(svg, progressCodes, code, mapTheme);
      } else {
        addCityMarker(svg, slot, code, elements);
      }
    }
    raiseLabels(svg, progressMode, mapTheme);
    return true;
  }

  function renderChina(slot) {
    if (typeof CHINA_MAP_SVG === 'undefined') return false;
    slot.innerHTML = CHINA_MAP_SVG;
    var svg = slot.querySelector('svg');
    if (!svg) return false;
    var id = slot.dataset.region || '';
    var el = svg.querySelector('#' + id);
    if (el) markChinaSvg(svg, [el], slot.dataset.shortLabel || id.replace(/^cn_/, '').toUpperCase());
    return true;
  }

  function renderWorld(slot) {
    slot.innerHTML = '<div class="article-map-world"><b>RunWorld Map</b><span>' + (slot.dataset.label || 'RunWorld') + '</span></div>';
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
