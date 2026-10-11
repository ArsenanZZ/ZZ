/* Render the site's existing China geography with a 青海西宁 callout. */
const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:860},deviceScaleFactor:1.5});
 const geo=fs.readFileSync(path.join(root,'run50/china-map-svg.js'),'utf8');
 const cn=fs.readFileSync(path.join(root,'CN/index.html'),'utf8');
 const provinceBlock=cn.match(/const CHINA_PROVINCES = (\{[\s\S]*?\n      \});/)[1];
 const dotBlock=cn.match(/const CHINA_CITY_DOTS = (\[[\s\S]*?\n      \]);/)[1].replace(/storyHref\('[^']+'\)/g,'null');
 await page.setContent('<html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}#map{width:1200px;height:860px}svg{display:block;width:1200px;height:860px;font-family:"Microsoft YaHei",sans-serif}</style></head><body><div id="map"></div></body></html>');
 await page.addScriptTag({content:geo+';window.mapSvg=CHINA_MAP_SVG;window.labels=_CN_LABELS;window.provinces='+provinceBlock+';window.cityDots='+dotBlock});
 const emblem='data:image/svg+xml;base64,'+fs.readFileSync(path.join(root,'assets/runcn-qinghai-2026/qinghai-map-emblem.svg')).toString('base64');
 await page.evaluate((emblem)=>{
  const slot=document.getElementById('map');slot.innerHTML=window.mapSvg;
  const svg=slot.querySelector('svg');svg.setAttribute('viewBox','0 0 800 575');svg.removeAttribute('style');
  const ns='http://www.w3.org/2000/svg';
  const add=(tag,attrs,text)=>{const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text)el.textContent=text;svg.appendChild(el);return el;};
  svg.querySelectorAll('text').forEach(x=>x.remove());
  svg.querySelectorAll('path[id^="bg_"]').forEach(x=>{x.setAttribute('fill','#f0ede4');x.setAttribute('stroke','#d9dbd1');x.setAttribute('stroke-width','.5');});
  svg.querySelectorAll('path[id^="cn_"]').forEach(x=>{
   const palette={'#ff6b4a':'#dba58b','#ffbe3c':'#dfc58d','#45af55':'#b1c5a7','#a65dd2':'#bbaecc','#36a6b5':'#94bac1'};const original=window.provinces[x.id]?.[1];x.style.fill=original?(palette[original]||original):'#e9e5d9';if(window.provinces[x.id]){const raw=window.provinces[x.id][1];const h=raw.replace('#','');if(h.length===6){const rgb=[0,2,4].map((v,i)=>Math.round(parseInt(h.slice(v,v+2),16)*.43+[242,237,222][i]*.57));x.style.fill='rgb('+rgb.join(',')+')';}}x.style.stroke='#89968f';x.style.strokeWidth='.65';
  });
  const gz=svg.querySelector('#cn_qinghai');gz.style.fill='#315f88';gz.style.stroke='#315f88';gz.style.strokeWidth='2';
  // Place labels inside the actual province paths, rather than old approximate coordinates.
  const names={gansu:'甘肃',qinghai:'青海',guangxi:'广西',guizhou:'贵州',chongqing:'重庆',beijing:'北京',fujian:'福建',anhui:'安徽',guangdong:'广东',tibet:'西藏',xinjiang:'新疆',hainan:'海南',ningxia:'宁夏',shaanxi:'陕西',shanxi:'山西',hubei:'湖北',hunan:'湖南',sichuan:'四川',yunnan:'云南',hebei:'河北',henan:'河南',liaoning:'辽宁',shandong:'山东',tianjin:'天津',jiangxi:'江西',jiangsu:'江苏',shanghai:'上海',zhejiang:'浙江',jilin:'吉林',innermongolia:'内蒙古',heilongjiang:'黑龙江',taiwan:'台湾',macao:'澳门',hongkong:'香港'};
  const labels=[];
  for(const [short,name] of Object.entries(names)){
   const id='cn_'+short,shape=svg.querySelector('#'+id);if(!shape)continue;
   if(['beijing','tianjin','shanghai','hongkong','macao'].includes(short))continue;
   const box=shape.getBBox(),length=shape.getTotalLength();
   const edge=Array.from({length:300},(_,i)=>shape.getPointAtLength(length*i/300));
   let best=null,score=-Infinity;
   for(let y=box.y+2;y<box.y+box.height;y+=3)for(let x=box.x+2;x<box.x+box.width;x+=3){
    if(!shape.isPointInFill(new DOMPoint(x,y)))continue;
    const distance=Math.min(...edge.map(p=>Math.hypot(p.x-x,p.y-y)));
    const s=distance-.06*Math.hypot(x-(box.x+box.width/2),y-(box.y+box.height/2));
    if(s>score){score=s;best={x,y};}
   }
   if(best)labels.push({id,name,...best,size:short==='qinghai'?22:short==='xinjiang'?20:short==='ningxia'?13:16});
  }
  const active=labels.find(l=>l.id==='cn_qinghai');if(active){active.x=306;active.y=299;}
  window.provinceLabels=labels;
  add('text',{x:35,y:40,'font-size':22,'font-family':'Noto Serif SC, SimSun, serif','font-weight':'800',fill:'#163e47'},'RunCN · 青海西宁');
  add('text',{x:35,y:65,'font-size':11,fill:'#365e66'},'2026.09.06 · 第30站');
  window.cityDots.forEach(([city,,lat,lon])=>{if(city!=='西宁')add('circle',{cx:(lon-70)*11.8,cy:(55-lat)*15,r:2.8,fill:'#ba6b50',stroke:'#fff8e8','stroke-width':.9});});
  window.provinceLabels.forEach(({id,name,x,y,size})=>add('text',{x,y,'font-size':size,'dominant-baseline':'middle','font-family':id==='cn_qinghai'?'Noto Serif SC, SimSun, serif':'KaiTi, STKaiti, serif','font-weight':id==='cn_qinghai'?'800':'600','text-anchor':'middle',fill:id==='cn_qinghai'?'#fff6df':window.provinces[id]?'#344d54':'#87918b','paint-order':'stroke',stroke:id==='cn_qinghai'?'#315f88':'#f5f0e4','stroke-width':id==='cn_qinghai'?1:.8},name));
  // Small coastal municipalities use an uncluttered external label column.
  const external=[['北京',116.4,39.9,669,254],['天津',117.2,39.1,690,280],['上海',121.47,31.23,693,378],['香港',114.17,22.3,647,508],['澳门',113.54,22.2,647,533]];
  external.forEach(([name,lon,lat,tx,ty])=>{const px=(lon-70)*11.8,py=(55-lat)*15;add('path',{d:`M${px} ${py} L${tx-18} ${ty} L${tx-5} ${ty}`,fill:'none',stroke:'#8e9a95','stroke-width':.75});add('text',{x:tx,y:ty,'dominant-baseline':'middle','font-size':14,'font-family':'KaiTi, STKaiti, serif',fill:'#536a71'},name);});
  // Existing site projection: x=(lon-70)*11.8, y=(55-lat)*15.
  const x=(101.7782-70)*11.8,y=(55-36.6171)*15;
  add('circle',{cx:x,cy:y,r:13,fill:'#fff4b3',opacity:.7});
  const points=Array.from({length:10},(_,i)=>{const a=-Math.PI/2+i*Math.PI/5,r=i%2?4.5:10;return (x+Math.cos(a)*r)+','+(y+Math.sin(a)*r)}).join(' ');
  add('polygon',{points,fill:'#e95532',stroke:'#fffdf0','stroke-width':1.8});
  add('path',{d:`M 182 487 C 205 398 275 340 ${x-10} ${y+8}`,fill:'none',stroke:'#a34723','stroke-width':2.6});
  add('image',{href:emblem,x:32,y:417,width:175,height:125});
  add('text',{x:119,y:565,'text-anchor':'middle','font-size':24,'font-family':'Noto Serif SC, SimSun, serif','font-weight':'800',fill:'#173d48'},'西宁');
 },emblem);
 await page.evaluate(()=>document.fonts.ready);
 await page.locator('#map').screenshot({path:path.join(root,'assets/runcn-qinghai-2026/map-qinghai-xining-20261011.jpg')});
 await browser.close();
})();
