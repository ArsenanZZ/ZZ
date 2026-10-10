/* Render the site's existing China geography with a Guizhou/Liupanshui callout. */
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
 const emblem='data:image/png;base64,'+fs.readFileSync(path.join(root,'assets/runcn-chuxiong-2026/chuxiong-map-emblem.png')).toString('base64');
 await page.evaluate((emblem)=>{
  const slot=document.getElementById('map');slot.innerHTML=window.mapSvg;
  const svg=slot.querySelector('svg');svg.setAttribute('viewBox','0 0 800 575');svg.removeAttribute('style');
  const ns='http://www.w3.org/2000/svg';
  const add=(tag,attrs,text)=>{const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text)el.textContent=text;svg.appendChild(el);return el;};
  svg.querySelectorAll('text').forEach(x=>x.remove());
  svg.querySelectorAll('path[id^="bg_"]').forEach(x=>{x.setAttribute('fill','#ece9db');x.setAttribute('stroke','#c1c7bd');x.setAttribute('stroke-width','.5');});
  svg.querySelectorAll('path[id^="cn_"]').forEach(x=>{
   x.style.fill=window.provinces[x.id]?.[1]||'#e7e3d8';x.style.stroke='#647975';x.style.strokeWidth='.7';
  });
  const gz=svg.querySelector('#cn_yunnan');gz.style.fill='#ed7553';gz.style.stroke='#9f3c26';gz.style.strokeWidth='2';
  Object.entries(window.labels).forEach(([id,[x,y,size]])=>{
   if(!size)return;const province=window.provinces[id];if(province)add('text',{x,y,'font-size':10,'text-anchor':'middle',fill:'#253b46'},province[0]);
  });
  add('text',{x:35,y:40,'font-size':21,'font-weight':'bold',fill:'#163e47'},'RunCN · 云南楚雄');
  add('text',{x:35,y:65,'font-size':11,fill:'#365e66'},'2026.08.02 · 第28站');
  window.cityDots.forEach(([city,,lat,lon])=>{if(city!=='楚雄')add('circle',{cx:(lon-70)*11.8,cy:(55-lat)*15,r:3.7,fill:'#ef6451',stroke:'#fff8e8','stroke-width':1});});
  // Existing site projection: x=(lon-70)*11.8, y=(55-lat)*15.
  const x=(101.5458-70)*11.8,y=(55-25.0329)*15;
  add('circle',{cx:x,cy:y,r:13,fill:'#fff4b3',opacity:.7});
  const points=Array.from({length:10},(_,i)=>{const a=-Math.PI/2+i*Math.PI/5,r=i%2?4.5:10;return (x+Math.cos(a)*r)+','+(y+Math.sin(a)*r)}).join(' ');
  add('polygon',{points,fill:'#e95532',stroke:'#fffdf0','stroke-width':1.8});
  add('path',{d:`M 170 505 C 240 520 300 468 ${x-10} ${y+8}`,fill:'none',stroke:'#a34723','stroke-width':2.6});
  add('image',{href:emblem,x:66,y:335,width:120,height:210});
  add('text',{x:126,y:564,'text-anchor':'middle','font-size':22,'font-weight':'bold',fill:'#173d48'},'楚雄');
 },emblem);
 await page.locator('#map').screenshot({path:path.join(root,'assets/runcn-chuxiong-2026/map-yunnan-chuxiong.jpg')});
 await browser.close();
})();
