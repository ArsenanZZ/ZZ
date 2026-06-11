// China Province Map — accurate boundaries fetched from open GeoJSON
const _CHINA_GEO_URL = 'https://raw.githubusercontent.com/longwosion/geojson-map-china/master/china.json';

const _CP_ID = {
  '新疆维吾尔自治区':'cn_xinjiang','西藏自治区':'cn_tibet',
  '内蒙古自治区':'cn_innermongolia','青海省':'cn_qinghai',
  '四川省':'cn_sichuan','黑龙江省':'cn_heilongjiang','甘肃省':'cn_gansu',
  '云南省':'cn_yunnan','广西壮族自治区':'cn_guangxi','湖南省':'cn_hunan',
  '陕西省':'cn_shaanxi','广东省':'cn_guangdong','吉林省':'cn_jilin',
  '河北省':'cn_hebei','湖北省':'cn_hubei','贵州省':'cn_guizhou',
  '山东省':'cn_shandong','江西省':'cn_jiangxi','河南省':'cn_henan',
  '辽宁省':'cn_liaoning','山西省':'cn_shanxi','安徽省':'cn_anhui',
  '福建省':'cn_fujian','浙江省':'cn_zhejiang','江苏省':'cn_jiangsu',
  '重庆市':'cn_chongqing','宁夏回族自治区':'cn_ningxia','海南省':'cn_hainan',
  '台湾省':'cn_taiwan','北京市':'cn_beijing','天津市':'cn_tianjin',
  '上海市':'cn_shanghai','香港特别行政区':'cn_hongkong','澳门特别行政区':'cn_macao',
};

// Color index (0-5) per province — preserves original graph coloring
const _CN_CI = {
  cn_xinjiang:0,cn_tibet:1,cn_qinghai:2,cn_innermongolia:3,
  cn_heilongjiang:0,cn_jilin:1,cn_liaoning:2,cn_gansu:4,
  cn_ningxia:5,cn_shaanxi:1,cn_shanxi:0,cn_hebei:5,
  cn_beijing:2,cn_tianjin:1,cn_shandong:3,cn_henan:4,
  cn_hubei:0,cn_anhui:2,cn_jiangsu:4,cn_zhejiang:3,
  cn_shanghai:5,cn_chongqing:5,cn_sichuan:3,cn_guizhou:1,
  cn_yunnan:4,cn_hunan:2,cn_jiangxi:1,cn_fujian:4,
  cn_guangdong:0,cn_guangxi:3,cn_hongkong:1,cn_hainan:2,
  cn_taiwan:4,cn_macao:3,
};

function _cnProj(lon, lat) {
  return [(lon - 70) * 11.8, (55 - lat) * 13.5];
}

function _geoToPath(geo) {
  const polys = geo.type === 'Polygon' ? [geo.coordinates] : geo.coordinates;
  return polys.map(poly =>
    poly.map(ring =>
      'M' + ring.map(([lo, la]) => {
        const [x, y] = _cnProj(lo, la);
        return x.toFixed(1) + ',' + y.toFixed(1);
      }).join('L') + 'Z'
    ).join(' ')
  ).join(' ');
}

async function renderChinaMap(slotId, opts) {
  const slot = document.getElementById(slotId);
  if (!slot) return;
  opts = opts || {};
  const pal = opts.colors || ['#d4614a','#e89838','#98c038','#5ca860','#3898a8','#9068c0'];
  const cities = opts.cities || [];
  const NS = 'http://www.w3.org/2000/svg';

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('id', 'cn-map-master');
  svg.setAttribute('viewBox', '0 0 800 560');
  svg.style.cssText = 'width:100%;height:auto;display:block';
  slot.innerHTML = '';
  slot.appendChild(svg);

  const wait = document.createElementNS(NS, 'text');
  wait.setAttribute('x', '400'); wait.setAttribute('y', '280');
  wait.setAttribute('text-anchor', 'middle'); wait.setAttribute('fill', '#aaa'); wait.setAttribute('font-size', '14');
  wait.textContent = '加载地图中…';
  svg.appendChild(wait);

  let geo;
  try {
    const r = await fetch(_CHINA_GEO_URL);
    if (!r.ok) throw new Error(r.status);
    geo = await r.json();
  } catch (e) {
    wait.textContent = '地图加载失败';
    return;
  }
  svg.removeChild(wait);

  for (const feat of geo.features) {
    const id = _CP_ID[feat.properties.name];
    if (!id || !feat.geometry) continue;
    const ci = _CN_CI[id] !== undefined ? _CN_CI[id] : 0;
    const path = document.createElementNS(NS, 'path');
    path.setAttribute('id', id);
    path.setAttribute('d', _geoToPath(feat.geometry));
    path.setAttribute('fill', pal[ci % pal.length]);
    path.setAttribute('stroke', '#fff');
    path.setAttribute('stroke-width', '1');
    path.setAttribute('stroke-linejoin', 'round');
    path.style.cursor = 'pointer';
    path.addEventListener('mouseover', () => { path.style.opacity = '0.8'; });
    path.addEventListener('mouseout', () => { path.style.opacity = '1'; });
    svg.appendChild(path);
  }

  cities.forEach(c => {
    const [cx, cy] = _cnProj(c.lon, c.lat);
    const glow = document.createElementNS(NS, 'circle');
    glow.setAttribute('cx', cx.toFixed(1)); glow.setAttribute('cy', cy.toFixed(1));
    glow.setAttribute('r', '10'); glow.setAttribute('fill', 'rgba(255,59,48,0.3)');
    glow.style.animation = 'pulse-glow 2s infinite alternate';
    glow.style.pointerEvents = 'none';
    svg.appendChild(glow);

    const dot = document.createElementNS(NS, 'circle');
    dot.setAttribute('cx', cx.toFixed(1)); dot.setAttribute('cy', cy.toFixed(1));
    dot.setAttribute('r', '5'); dot.setAttribute('fill', '#ff3b30');
    dot.setAttribute('stroke', '#fff'); dot.setAttribute('stroke-width', '1.5');
    if (c.url) { dot.style.cursor = 'pointer'; dot.addEventListener('click', () => window.location.href = c.url); }
    svg.appendChild(dot);

    const lbl = document.createElementNS(NS, 'text');
    lbl.setAttribute('x', (cx + 8).toFixed(1)); lbl.setAttribute('y', (cy - 4).toFixed(1));
    lbl.setAttribute('font-size', '11'); lbl.setAttribute('fill', '#333');
    lbl.setAttribute('font-family', '-apple-system,sans-serif'); lbl.setAttribute('font-weight', '600');
    lbl.textContent = c.name;
    svg.appendChild(lbl);
  });
}
