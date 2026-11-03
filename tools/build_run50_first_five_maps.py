"""Historical first-four-state maps, preserving the shared US geometry."""
from pathlib import Path
import base64,json
import build_wechat_run50_maps as base
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/run50-first-five-20261102'
JOBS=[
 ('kentucky','KY',1,'Louisville','kentucky-icon.png',[1025,800,160,165],1105,995,'肯塔基 · 路易斯维尔','M1105 805 C1105 720,1220 680,${x-7} ${y+19}'),
 ('cleveland','OH',2,'Cleveland','cleveland-icon.png',[1505,575,230,180],1620,795,'俄亥俄 · 克利夫兰','M1515 650 C1480 585,1450 490,${x+18} ${y+10}'),
 ('new-york','NY',3,'New York City','../new-york-editorial-20261013/liberty.webp',[1580,575,170,240],1665,850,'纽约市','M1620 580 C1610 515,1550 460,${x+20} ${y+6}'),
 ('san-francisco','CA',4,'San Francisco','sf-icon.png',[85,550,245,140],207,730,'加州 · 旧金山','M280 610 C320 570,330 530,${x-14} ${y+15}')
]
def main():
 base.CITY_DOTS[:]=[d for d in base.CITY_DOTS if d[1]!='Williamson']
 for name,state,count,city,icon,box,cx,cy,label,curve in JOBS:
  html=base.build_html(base.MapConfig('',state,count,city))
  mime='image/webp' if icon.endswith('.webp') else 'image/png'
  image=base64.b64encode((ASSET/icon).read_bytes()).decode()
  cfg=dict(state=state,city=city,box=box,cx=cx,cy=cy,label=label,count=count,uri='data:'+mime+';base64,'+image)
  js=r'''
const cfg=CONFIG,svg=document.getElementById('us-map-master'),ns='http://www.w3.org/2000/svg';
const add=(tag,attrs,text='')=>{const e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));e.textContent=text;svg.appendChild(e);return e};
document.getElementById('current-state-outline')?.remove();
document.querySelectorAll('#city-dots-group text').forEach(e=>e.remove());
if(cfg.state==='CA')document.querySelectorAll('svg path').forEach(e=>{const b=e.getBBox();if(b.x<200&&b.y>350&&b.y<500&&b.height>100)e.remove()});
if(cfg.state==='KY')document.getElementById('map_ATLANTIC_OCEAN')?.remove();
if(['NY','OH'].includes(cfg.state))document.querySelectorAll('svg path[id]').forEach(e=>{const b=e.getBBox();if(b.x>1450&&b.y>500&&b.y<650&&b.height>150&&b.width<250)e.remove()});
const dot=CITY_DOTS.find(d=>d[0]===cfg.state&&d[1]===cfg.city),pt=SPECIAL_POSITIONS[cfg.state+':'+cfg.city]||projectAlbers(dot[2],dot[3]);
const x=pt.x,y=pt.y;
add('path',{d:`CURVE`,fill:'none',stroke:'#a46b35','stroke-width':3,'stroke-linecap':'round'});
add('image',{href:cfg.uri,x:cfg.box[0],y:cfg.box[1],width:cfg.box[2],height:cfg.box[3]});
add('text',{x:cfg.cx,y:cfg.cy,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial','font-size':27,'font-weight':800,fill:'#24475b'},cfg.label);
add('text',{x:cfg.cx,y:cfg.cy+28,'text-anchor':'middle','font-family':'Arial','font-size':20,'font-weight':600,fill:'#775831'},'RUN50 '+String(cfg.count).padStart(2,'0'));
svg.appendChild(document.getElementById('city-dots-group'));
window.mapValidation={current:CURRENT,states:RUN_STATES,star:pt};
'''.replace('CONFIG',json.dumps(cfg,ensure_ascii=False)).replace('CURVE',curve)
  html=html.replace('border-radius:10px','border-radius:0').replace('border:1px solid #dde5ec','border:0')
  html=html.replace('</body>','<script>'+js+'</script></body>')
  (ROOT/f'tmp/{name}-review-map.html').write_text(html,encoding='utf8')
if __name__=='__main__':main()
