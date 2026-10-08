"""Keep the established Run50 geography; add city-specific editorial callouts."""
from pathlib import Path
import json
import build_wechat_run50_maps as base

ROOT=Path(__file__).resolve().parents[1]
CONFIG=[
 ('blue-ridge-marathon','VA',24,'Roanoke','弗吉尼亚','罗阿诺克',1480,690,'#f3bd3d','mountain'),
 ('kentucky-derby-marathon-2025','KY',24,'Louisville','肯塔基','路易斯维尔',1470,665,'#e376a6','horseshoe'),
 ('fargo-marathon','ND',25,'Fargo','北达科他','法戈',1130,85,'#f3bd3d','wheat'),
 ('hell-on-gravel-marathon','KS',26,'El Dorado','堪萨斯','埃尔多拉多',1000,855,'#f3cf42','sunflower'),
 ('mad-marathon','VT',27,'Warren','佛蒙特','沃伦',1125,80,'#dc82ad','bridge'),
 ('rocket-city-marathon','AL',28,'Huntsville','阿拉巴马','亨茨维尔',1055,820,'#688dd1','rocket'),
]

# Small vector illustrations extend the site's existing outlined city-icon system.
ICONS={
 'rocket':'<path d="M72 96L88 64 88 25Q96 7 104 0Q112 7 120 25L120 64 136 96 116 87 92 87Z" fill="#fff5d8"/><path d="M88 25Q104 5 120 25L120 35 88 35Z" fill="#d25e3d"/><path d="M95 90Q104 124 113 90" fill="#f4b63d"/><circle cx="104" cy="49" r="10" fill="#508ca8"/><path d="M94 69H114M94 77H114" fill="none"/>',
 'mountain':'<path d="M18 99L70 40 95 65 135 23 192 99Z" fill="#5484a5"/><path d="M45 72L70 40 93 66 73 58Z M113 49L135 23 157 51 136 43Z" fill="#fff4d4"/><path d="M92 99Q132 86 110 80T128 62" fill="none" stroke="#f5ca63" stroke-width="5"/><path d="M136 0L141 12 154 13 144 22 147 35 136 28 125 35 128 22 118 13 131 12Z" fill="#f2bb38"/>',
 'horseshoe':'<path d="M62 10L77 16Q49 68 83 85Q108 97 131 76Q151 57 129 15L145 10Q180 72 139 105Q105 133 65 106Q26 79 62 10Z" fill="#d9a947"/><path d="M61 35L69 39M55 56L65 57M60 79L69 75M75 96L81 87M97 104L98 94M120 100L116 91M140 83L132 77M148 60L138 59M141 36L132 41" stroke="#fff3ca" stroke-width="5"/><circle cx="107" cy="36" r="22" fill="#bf5348"/><path d="M97 32Q107 16 119 32T100 47Q91 38 107 33" fill="none" stroke="#7c3432"/><path d="M83 49L92 28 92 51M127 50L128 30 138 53" fill="#568154"/>',
 'wheat':'<path d="M93 111V42L124 22 154 43V111Z" fill="#bb6c43"/><path d="M86 43L124 15 161 43Z" fill="#355b63"/><path d="M113 110V71H138V110" fill="#f7e6b0"/><path d="M52 112V13M34 112L24 39M70 112L78 38" fill="none" stroke="#936d24" stroke-width="4"/><g fill="#efc251"><ellipse cx="42" cy="31" rx="6" ry="14" transform="rotate(-35 42 31)"/><ellipse cx="62" cy="40" rx="6" ry="14" transform="rotate(35 62 40)"/><ellipse cx="42" cy="53" rx="6" ry="14" transform="rotate(-35 42 53)"/><ellipse cx="62" cy="64" rx="6" ry="14" transform="rotate(35 62 64)"/><ellipse cx="52" cy="15" rx="6" ry="14"/></g>',
 'bridge':'<path d="M10 100L66 35 100 70 137 18 195 100Z" fill="#4d7f5a"/><path d="M57 109V76L101 49 148 77V109Z" fill="#b24c3d"/><path d="M48 77L101 44 157 77" fill="none" stroke="#fff0bd" stroke-width="5"/><path d="M86 109V80H115V109" fill="#354a43"/><path d="M151 40L154 25 144 28 149 16 140 9 153 11 156 0 164 11 177 7 172 20 184 25 172 31 171 45 162 38 159 53" fill="#edb641"/>',
}
petals=''.join(f'<ellipse cx="102" cy="25" rx="11" ry="25" transform="rotate({i*30} 102 57)" fill="#f3be39"/>' for i in range(12))
ICONS['sunflower']='<path d="M102 84V120M102 113Q57 111 61 86Q94 85 102 110M103 102Q125 78 147 89Q144 110 103 113" fill="#52864a"/>'+petals+'<circle cx="102" cy="57" r="24" fill="#674a2d"/><circle cx="102" cy="57" r="16" fill="#966331" stroke-dasharray="2 4"/>'

def main():
 base.SPECIAL_POSITIONS['VT:Warren']={'x':1469,'y':303}
 for slug,abbr,count,city,cn,city_cn,x,y,color,icon in CONFIG:
  cfg=base.MapConfig('',abbr,count,city)
  html=base.build_html(cfg)
  callout=dict(slug=slug,abbr=abbr,city=city,cn=cn,city_cn=city_cn,x=x,y=y,color=color,icon=ICONS[icon],number=1 if abbr=='KY' else count)
  script=r'''
const cfg=CALLOUT;
document.querySelectorAll('svg path').forEach(e=>e.style.transition='none');
const svg=document.querySelector('#us-map-master'), ns='http://www.w3.org/2000/svg';
const add=(name,attrs,parent=svg,text='')=>{const e=document.createElementNS(ns,name);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);e.textContent=text;parent.appendChild(e);return e;};
const dot=CITY_DOTS.find(d=>d[0]===cfg.abbr&&d[1]===cfg.city);
const p=SPECIAL_POSITIONS[cfg.abbr+':'+cfg.city]||projectAlbers(dot[2],dot[3]);
document.querySelector('#city-dots-group text')?.remove();
(STATE_PATHS[cfg.abbr]||[]).forEach(id=>document.getElementById('map_'+id).style.fill=cfg.color);
document.querySelectorAll('#current-state-outline path').forEach(e=>{e.style.fill='none';e.setAttribute('stroke','#635027');e.setAttribute('stroke-width','3.5');});
const x=cfg.x,y=cfg.y;
const startX=x+100,startY=y+45;
const d=`M ${startX} ${startY} Q ${p.x+110} ${startY} ${p.x} ${p.y}`;
add('path',{d,fill:'none',stroke:'#fff7dc','stroke-width':7,'stroke-linecap':'round'});
add('path',{d,fill:'none',stroke:'#8b6733','stroke-width':3,'stroke-linecap':'round'});
// Move annotation into open water; omit only the ocean title beneath it.
if (['AL','KS'].includes(cfg.abbr)) document.querySelectorAll('[id="map_ATLANTIC_OCEAN"]').forEach(e=>e.remove());
if (['VA','KY'].includes(cfg.abbr)) document.querySelectorAll('[id="map_gulf_of_mexico"]').forEach(e=>e.remove());
const art=add('g',{transform:`translate(${x-10} ${y}) scale(1.1)`,stroke:'#58492d','stroke-width':'2.4','stroke-linejoin':'round','stroke-linecap':'round'});art.innerHTML=cfg.icon;
add('text',{x:x+102,y:y+153,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial,sans-serif','font-size':31,'font-weight':800,fill:'#24475b'},svg,cfg.cn);
add('text',{x:x+102,y:y+183,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial,sans-serif','font-size':24,'font-weight':600,fill:'#5b472b'},svg,cfg.city_cn+' · RUN50 '+cfg.number);
svg.appendChild(document.querySelector('#city-dots-group'));
add('circle',{cx:p.x,cy:p.y,r:22,fill:'none',stroke:'#fff5cc','stroke-width':4});
window.calloutValidation={slug:cfg.slug,city:cfg.city,abbr:cfg.abbr,x:p.x,y:p.y,count:RUN_STATES.length};
'''.replace('CALLOUT',json.dumps(callout,ensure_ascii=False))
  html=html.replace('</body>','<script>'+script+'</script></body>')
  (ROOT/f'tmp/{slug}-callout-map.html').write_text(html,encoding='utf8')
 (ROOT/'tmp/six-callout-slugs.json').write_text(json.dumps([x[0] for x in CONFIG]),encoding='utf8')

if __name__=='__main__':main()
