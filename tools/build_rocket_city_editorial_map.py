"""Rocket City map: established geography, a single state boundary and textured icon."""
from pathlib import Path
import base64
import build_wechat_run50_maps as base

ROOT = Path(__file__).resolve().parents[1]

def main():
    html = base.build_html(base.MapConfig('', 'AL', 28, 'Huntsville'))
    icon = base64.b64encode((ROOT / 'assets/rocket-city-map-saturn-v-20261102.png').read_bytes()).decode()
    script = r'''
const svg=document.querySelector('#us-map-master'), ns='http://www.w3.org/2000/svg';
const add=(t,a,text='')=>{const e=document.createElementNS(ns,t);Object.entries(a).forEach(([k,v])=>e.setAttribute(k,v));e.textContent=text;svg.appendChild(e);return e;};
document.querySelectorAll('svg path').forEach(e=>e.style.transition='none');
// The two mapped AL paths are a filled shape and its inset stroke fragment.
// Cloning both as outlines produces the old doubled, offset border.
document.querySelector('#current-state-outline').remove();
document.querySelector('#city-dots-group text').remove();
const state=document.getElementById('map_alabama');
state.style.fill='#688dd1';
const fragment=document.getElementById('map_Missispi');
fragment.style.fill='#688dd1';
const dot=CITY_DOTS.find(d=>d[0]==='AL'&&d[1]==='Huntsville');
const p=projectAlbers(dot[2],dot[3]);
document.querySelectorAll('[id="map_ATLANTIC_OCEAN"]').forEach(e=>e.remove());
// Place the landmark in open gulf water; lead into the star from the west,
// keeping Alabama's abbreviation and neighbouring labels unobstructed.
add('path',{d:`M 1182 825 C 1120 810, 1130 720, ${p.x-12} ${p.y+12}`,fill:'none',stroke:'#a47732','stroke-width':3,'stroke-linecap':'round'});
add('image',{href:'data:image/png;base64,ICON',x:1110,y:815,width:145,height:180});
add('text',{x:1182,y:1018,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial','font-size':28,'font-weight':800,fill:'#24475b'},'阿拉巴马');
add('text',{x:1182,y:1044,'text-anchor':'middle','font-family':'Microsoft YaHei,Arial','font-size':21,'font-weight':600,fill:'#5b472b'},'亨茨维尔 · RUN50 28');
svg.appendChild(document.querySelector('#city-dots-group'));
window.mapValidation={count:RUN_STATES.length,current:CURRENT,star:p};
'''.replace('ICON', icon)
    html = html.replace('</body>', '<script>'+script+'</script></body>')
    (ROOT/'tmp/rocket-city-textured-map.html').write_text(html, encoding='utf8')

if __name__ == '__main__':
    main()
