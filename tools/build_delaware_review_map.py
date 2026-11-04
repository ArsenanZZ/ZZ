from pathlib import Path
import base64,json
import build_wechat_run50_maps as base
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/delaware-review-20261103'
def main():
 base.RUN50_ORDER.append('DE')
 base.CITY_DOTS.append(('DE','Wilmington',39.7391,-75.5398))
 base.COLORS['DE']='#e89838'
 # The hand-drawn northeastern coast differs from the approximate projection.
 # Place Wilmington inside northern Delaware, rather than in adjacent Pennsylvania.
 base.SPECIAL_POSITIONS['DE:Wilmington']={'x':1435,'y':453}
 html=base.build_html(base.MapConfig('','DE',30,'Wilmington'))
 uri='data:image/png;base64,'+base64.b64encode((ASSET/'bridge-icon.png').read_bytes()).decode()
 js=r'''
const svg=document.getElementById('us-map-master'),ns='http://www.w3.org/2000/svg';
const add=(tag,attrs,text='')=>{const e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));e.textContent=text;svg.appendChild(e);return e;};
document.getElementById('current-state-outline')?.remove();
document.querySelectorAll('#city-dots-group text').forEach(e=>e.remove());
svg.querySelectorAll('path[id]').forEach(e=>{const b=e.getBBox();if(b.x>1450&&b.y>500&&b.y<650&&b.height>150&&b.width<250)e.remove()});
add('path',{d:'M1605 652 C1620 590 1430 560 1440 468',fill:'none',stroke:'#92633c','stroke-width':2.8,'stroke-linecap':'round'});
add('image',{href:URI,x:1503,y:650,width:255,height:173});
add('text',{x:1630,y:855,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial','font-size':25,'font-weight':800,fill:'#24475b'},'特拉华 · 威尔明顿');
add('text',{x:1630,y:885,'text-anchor':'middle','font-family':'Arial','font-size':20,fill:'#775831'},'RUN50 30');
svg.appendChild(document.getElementById('city-dots-group'));
const de=document.getElementById('map_Massachusets_1_');
window.mapValidation={states:RUN_STATES.length,current:CURRENT,starInside:de.isPointInFill(new DOMPoint(1435,453))};
'''.replace('URI',json.dumps(uri))
 html=html.replace('border-radius:10px','border-radius:0').replace('border:1px solid #dde5ec','border:0')
 (ROOT/'tmp/delaware-reviewed-map.html').write_text(html.replace('</body>','<script>'+js+'</script></body>'),encoding='utf8')
if __name__=='__main__':main()

