const {chromium}=require('C:/Users/ZZ/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});
 const p=await b.newPage({viewport:{width:1200,height:704},deviceScaleFactor:1.5});
 await p.goto('file:///'+path.resolve('tmp/wechat-maine-editorial-map.html').replaceAll('\\','/'));
 await p.evaluate(()=>{
  const svg=document.querySelector('#us-map-master');document.querySelector('#mi-highlight-outline')?.remove();
  const ns='http://www.w3.org/2000/svg';
  function add(t,a){const e=document.createElementNS(ns,t);Object.entries(a).forEach(([k,v])=>e.setAttribute(k,v));svg.appendChild(e);return e}
  const star=svg.querySelector('#city-dots-group polygon[fill="#ffcc00"]');
  const pts=star.getAttribute('points').split(' ').map(x=>x.split(',').map(Number));const cx=pts.reduce((a,v)=>a+v[0],0)/10,cy=pts.reduce((a,v)=>a+v[1],0)/10;
  // Place the pine arrow over the Atlantic, with its tip linked directly to Sanford.
  add('path',{d:`M ${cx+10} ${cy} L 1584 298`,fill:'none',stroke:'#987335','stroke-width':3,'stroke-linecap':'round'});
  add('image',{href:'../assets/maine-editorial/map-callout-v2.png',x:1580,y:210,width:180,height:120});
 });
 await p.waitForTimeout(500);await p.locator('#map-slot').screenshot({path:'assets/maine-editorial/map.jpg',quality:92,type:'jpeg'});
 await b.close();
})();
