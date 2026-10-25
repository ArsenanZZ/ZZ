"""Atlantic City historical Run50 map: only the first 38 states."""
from pathlib import Path
import base64
import build_wechat_run50_maps as maps

ROOT=Path(__file__).resolve().parents[1]
def build():
    extra=[('DE','Wilmington',39.7391,-75.5398),('MN','Rochester',44.0121,-92.4802),('CT','Simsbury',41.8759,-72.8012),('RI','Woonsocket',42.0029,-71.5148),('MA','Holyoke',42.2043,-72.6162),('ME','Sanford',43.4392,-70.7742),('NE','Omaha',41.2565,-95.9345),('MD','Baltimore',39.2904,-76.6122),('NJ','Atlantic City',39.3643,-74.4229)]
    maps.RUN50_ORDER[:]=maps.RUN50_ORDER[:29]+[x[0] for x in extra]
    maps.CITY_DOTS.extend(extra)
    maps.COLORS.update(DE='#dba55b',MN='#7ea8bb',CT='#aa91c4',RI='#c97863',MA='#74aab1',ME='#dba28b',NE='#dbbc68',MD='#ab672f',NJ='#278e6e')
    html=maps.build_html(maps.MapConfig('map.jpg','NJ',38,'Atlantic City'))
    icon='data:image/webp;base64,'+base64.b64encode((ROOT/'assets/run50-atlantic-city-2026/landmark.webp').read_bytes()).decode()
    pointer='''
      ['map_STATES','map_OCEANS'].forEach(id=>document.getElementById(id)?.remove());
      const landmark=document.createElementNS('http://www.w3.org/2000/svg','g');
      landmark.id='atlantic-landmark';
      landmark.innerHTML=`<defs><marker id="atlantic-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M1 1 L5 3.5 L1 6" fill="none" stroke="#278e6e" stroke-width="1.4"/></marker></defs>
      <path d="M1560 662 C1620 590 1570 505 ${x+18} ${y+8}" fill="none" stroke="#278e6e" stroke-width="3.5" stroke-linecap="round" marker-end="url(#atlantic-arrow)"/>
      <image href="ICON" x="1440" y="660" width="260" height="174"/>
      <text x="1570" y="870" text-anchor="middle" fill="#244450" font-size="32" font-weight="bold" font-family="KaiTi,serif">新泽西 · 大西洋城</text>
      <text x="1570" y="905" text-anchor="middle" fill="#516770" font-size="22" font-family="Arial,sans-serif">2026.10.18 · RUN50 38</text>`;
      master.appendChild(landmark);
    '''.replace('ICON',icon)
    html=html.replace('addCurrentLabel(dotGroup,x,y);',pointer)
    html=html.replace('height:704px','height:690px').replace('padding:12px; background:#fff','padding:0; background:#f3efdf').replace('border-radius:10px','border-radius:0').replace('border:1px solid #dde5ec','border:0')
    out=ROOT/'tmp/atlantic-city-2026/map.html';out.write_text(html,encoding='utf8');print(out)
if __name__=='__main__':build()
