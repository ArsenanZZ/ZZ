"""Cumulative third-state map, with a Liberty landmark pointing to NYC."""
from pathlib import Path
import build_wechat_run50_maps as maps

ROOT=Path(__file__).resolve().parents[1]
def build():
 maps.CITY_DOTS[:]=[d for d in maps.CITY_DOTS if d[1]!='Williamson']
 html=maps.build_html(maps.MapConfig('map-new-york.jpg','NY',3,'New York City'))
 pointer='''
 const landmark=document.createElementNS('http://www.w3.org/2000/svg','g');
 landmark.id='nyc-landmark';
 landmark.innerHTML=`<defs><marker id="nyc-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M1 1 L6 4 L1 7" fill="none" stroke="#ad5639" stroke-width="1.5"/></marker></defs>
 <path d="M1680 563 Q1700 490 ${x+22} ${y+5}" stroke="#ad5639" stroke-width="4" fill="none" stroke-linecap="round" marker-end="url(#nyc-arrow)"/>
 <image href="/assets/new-york-editorial-20261013/liberty.webp" x="1610" y="565" width="160" height="245"/>
 <text x="1670" y="842" text-anchor="middle" fill="#193e4b" font-size="34" font-weight="bold" font-family="Georgia,serif">纽约市</text>
 <text x="1670" y="874" text-anchor="middle" fill="#193e4b" font-size="21" font-family="Arial,sans-serif">RUN50 03 · 2021</text>`;
 master.appendChild(landmark);
 '''
 html=html.replace('addCurrentLabel(dotGroup,x,y);',pointer)
 html=html.replace('width:1200px; height:704px','width:1200px; height:690px').replace('padding:12px; background:#fff','padding:0; background:#f3efdf').replace('border-radius:10px','border-radius:0').replace('border:1px solid #dde5ec','border:0')
 (ROOT/'tmp/new-york/map.html').write_text(html,encoding='utf-8')
if __name__=='__main__':build()
