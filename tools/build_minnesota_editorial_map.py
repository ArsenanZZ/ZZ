"""Render the established cumulative Run50 map with a Rochester landmark pointer."""
from pathlib import Path
import build_wechat_run50_maps as maps

ROOT = Path(__file__).resolve().parents[1]


def build():
    maps.RUN50_ORDER[:] = maps.RUN50_ORDER[:29] + ['DE', 'MN']
    maps.COLORS.update(DE='#e89838', MN='#527b91')
    maps.CITY_DOTS.extend([
        ('DE', 'Wilmington', 39.7391, -75.5398),
        ('MN', 'Rochester', 44.0121, -92.4802),
    ])
    html = maps.build_html(maps.MapConfig('map-minnesota.jpg', 'MN', 31, 'Rochester'))
    pointer = '''
      const landmark=document.createElementNS('http://www.w3.org/2000/svg','g');
      landmark.id='rochester-landmark';
      landmark.innerHTML=`
        <text x="995" y="280" text-anchor="middle" fill="#182d38" font-family="Segoe Print,Arial,sans-serif" font-size="38">MN</text><defs><marker id="landmark-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M1 1 L6 4 L1 7" fill="none" stroke="#9b4933" stroke-width="1.5" stroke-linecap="round"/></marker></defs>
        <path d="M1178 215 Q1080 206 ${x+13} ${y-25}" fill="none" stroke="#9b4933" stroke-width="4.5" stroke-linecap="round" marker-end="url(#landmark-arrow)"/>
        <g transform="translate(1190 79)" stroke="#263d46" stroke-width="3" stroke-linejoin="round">
          <path d="M0 151 V107 H32 V78 H45 V43 H56 V20 H66 V5 H75 V20 H86 V43 H99 V78 H111 V109 H140 V151 Z" fill="#c4a26c"/>
          <path d="M56 151 V43 H86 V151 M32 151 V107 H0 M111 151 V109 H140 M45 78 H99" fill="none"/>
          <path d="M63 36 V24 M75 36 V24 M54 69 V50 M66 69 V50 M79 69 V50 M91 69 V50 M52 97 V84 M66 97 V84 M80 97 V84 M94 97 V84 M42 139 V114 M12 139 V116 M25 139 V116 M120 139 V117 M132 139 V117" stroke="#485760"/>
          <path d="M63 151 V120 Q72 105 81 120 V151" fill="#244450"/>
          <path d="M-8 154 H148" stroke="#7f8d74" stroke-width="5"/>
        </g>
        <text x="1170" y="113" text-anchor="end" fill="#244a59" font-size="32" font-family="Georgia,serif" font-weight="bold">明尼苏达 · 罗切斯特</text>
        <text x="1170" y="151" text-anchor="end" fill="#244a59" font-size="21" font-family="Arial,sans-serif">RUN50 31 · MED CITY</text>
        <text x="1170" y="184" text-anchor="end" fill="#476779" font-size="20" font-family="Arial,sans-serif">Plummer Building</text>`;
      master.appendChild(landmark);
    '''
    html = html.replace('addCurrentLabel(dotGroup,x,y);', pointer)
    html = html.replace('width:1200px; height:704px', 'width:1200px; height:690px')
    html = html.replace('padding:12px; background:#fff', 'padding:0; background:#f3efdf')
    html = html.replace('border-radius:10px', 'border-radius:0').replace('border:1px solid #dde5ec', 'border:0')
    path = ROOT/'tmp/minnesota/map.html'
    path.parent.mkdir(exist_ok=True)
    path.write_text(html, encoding='utf-8')
    print(path)


if __name__ == '__main__':
    build()
