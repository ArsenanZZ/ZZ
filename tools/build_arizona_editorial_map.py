"""Run50 station 29: textured saguaro callout on the existing map geometry."""
from pathlib import Path
import base64
import build_wechat_run50_maps as base

ROOT = Path(__file__).resolve().parents[1]

def main():
    html = base.build_html(base.MapConfig('', 'AZ', 29, 'Buckeye'))
    icon = base64.b64encode((ROOT/'assets/arizona-map-saguaro-20261102.png').read_bytes()).decode()
    script = r'''
const svg=document.querySelector('#us-map-master'),ns='http://www.w3.org/2000/svg';
const add=(tag,attrs,text='')=>{const e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));e.textContent=text;svg.appendChild(e);return e};
document.querySelectorAll('svg path').forEach(e=>e.style.transition='none');
document.querySelector('#current-state-outline').remove();
document.querySelector('#city-dots-group text').remove();
const dot=CITY_DOTS.find(d=>d[0]==='AZ'&&d[1]==='Buckeye'),p=projectAlbers(dot[2],dot[3]);
// Pacific label is a scrambled SVG ID; remove only the label occupying this callout.
document.querySelectorAll('svg path').forEach(e=>{const b=e.getBBox();if(b.x<200&&b.y>350&&b.y<500&&b.height>100)e.remove()});
add('path',{d:`M 304 673 C 369 690, 405 700, ${p.x-14} ${p.y+7}`,fill:'none',stroke:'#9b7434','stroke-width':3,'stroke-linecap':'round'});
add('image',{href:'data:image/png;base64,ICON',x:175,y:485,width:160,height:225});
add('text',{x:255,y:735,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial','font-size':28,'font-weight':800,fill:'#24475b'},'亚利桑那');
add('text',{x:255,y:763,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial','font-size':21,'font-weight':600,fill:'#5b472b'},'巴克艾 · RUN50 29');
svg.appendChild(document.querySelector('#city-dots-group'));
window.mapValidation={count:RUN_STATES.length,current:CURRENT,star:p};
'''.replace('ICON',icon)
    html=html.replace('</body>','<script>'+script+'</script></body>')
    (ROOT/'tmp/arizona-textured-map.html').write_text(html,encoding='utf8')

if __name__=='__main__':
    main()
