"""Fourth-state map with a native SVG Golden Gate Bridge pointer."""
from pathlib import Path
import build_wechat_run50_maps as maps
ROOT=Path(__file__).resolve().parents[1]
def build():
 maps.CITY_DOTS[:]=[d for d in maps.CITY_DOTS if d[1]!='Williamson']
 html=maps.build_html(maps.MapConfig('map-san-francisco.jpg','CA',4,'San Francisco'))
 pointer='''
 // The source SVG's Pacific Ocean lettering has this misleading legacy ID.
 const ocean=document.getElementById('map_gulf_of_mexico');if(ocean)ocean.style.display='none';
 const landmark=document.createElementNS('http://www.w3.org/2000/svg','g');landmark.id='sf-landmark';
 landmark.innerHTML=`<defs><marker id="sf-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M1 1 L6 4 L1 7" fill="none" stroke="#ad5639" stroke-width="1.5"/></marker></defs>
 <path d="M275 610 Q350 595 ${x-18} ${y+18}" stroke="#ad5639" stroke-width="4" fill="none" stroke-linecap="round" marker-end="url(#sf-arrow)"/>
 <g transform="translate(75 574)" stroke="#aa412e" stroke-width="4" fill="none" stroke-linejoin="round">
 <path d="M0 107 H230 M0 116 H230" stroke="#254859"/><path d="M48 122 V8 H64 V122 M48 34 H64 M48 63 H64 M48 94 H64 M167 122 V8 H183 V122 M167 34 H183 M167 63 H183 M167 94 H183"/>
 <path d="M0 86 Q28 64 56 14 Q117 133 175 14 Q203 61 230 85"/>
 <path d="M12 78 V107 M26 62 V107 M40 39 V107 M76 48 V107 M90 67 V107 M104 77 V107 M118 81 V107 M132 77 V107 M146 62 V107 M160 42 V107 M192 42 V107 M207 65 V107 M221 79 V107" stroke-width="2"/>
 <path d="M0 130 Q25 122 50 130 T100 130 T150 130 T200 130 T230 130" stroke="#438c9e" stroke-width="3"/>
 </g><text x="355" y="572" text-anchor="middle" fill="#172b36" font-size="38" font-family="Segoe Print,Arial,sans-serif">CA</text>
 <text x="183" y="542" text-anchor="middle" fill="#365c69" font-size="19" font-family="Segoe Print,Arial,sans-serif">PACIFIC OCEAN</text>
 <text x="187" y="752" text-anchor="middle" fill="#193e4b" font-size="34" font-weight="bold" font-family="Georgia,serif">加州 · 旧金山</text>
 <text x="187" y="782" text-anchor="middle" fill="#193e4b" font-size="20" font-family="Arial,sans-serif">RUN50 04 · 2022</text>`;master.appendChild(landmark);
 '''
 html=html.replace('addCurrentLabel(dotGroup,x,y);',pointer).replace('width:1200px; height:704px','width:1200px; height:690px').replace('padding:12px; background:#fff','padding:0; background:#f3efdf').replace('border-radius:10px','border-radius:0').replace('border:1px solid #dde5ec','border:0')
 (ROOT/'tmp/san-francisco/map.html').write_text(html,encoding='utf-8')
if __name__=='__main__':build()
