// Render the established Run50 SVG with an editorial city callout.
// Usage: NODE_PATH=<playwright packages> node tools/build_wechat_michigan_editorial_map.cjs
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({channel:'chrome', headless:true});
  const page = await browser.newPage({viewport:{width:1200,height:704},deviceScaleFactor:1.5});
  await page.goto('file:///' + path.resolve('tmp/wechat-louisville-editorial-map.html').replaceAll('\\','/'));
  await page.evaluate(() => {
    const svg=document.querySelector('#us-map-master');
    document.querySelector('#mi-highlight-outline').remove();
    const ns='http://www.w3.org/2000/svg';
    const add=(name,attrs,parent=svg)=>{const e=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);parent.appendChild(e);return e;};
    const defs=add('defs',{});
    const filter=add('filter',{id:'paper-grain',x:'0',y:'0',width:'100%',height:'100%'},defs);
    add('feTurbulence',{type:'fractalNoise',baseFrequency:'.035',numOctaves:'3',seed:'21',stitchTiles:'stitch'},filter);
    add('rect',{width:'100%',height:'100%',filter:'url(#paper-grain)',opacity:'.065','pointer-events':'none'});
    const star=svg.querySelector('#city-dots-group polygon[fill="#ffcc00"]');
    const points=star.getAttribute('points').split(' ').map(p=>p.split(',').map(Number));
    const cx=points.reduce((a,p)=>a+p[0],0)/10, cy=points.reduce((a,p)=>a+p[1],0)/10;
    const tx=cx-220, ty=130;
    add('path',{d:`M ${tx+250} ${ty+36} Q ${cx-20} ${ty+95} ${cx-4} ${cy-24}`,fill:'none',stroke:'#15252c','stroke-width':'3','stroke-linecap':'round'});
    add('path',{d:`M ${cx-13} ${cy-29} L ${cx-4} ${cy-22} L ${cx-2} ${cy-34}`,fill:'none',stroke:'#15252c','stroke-width':'3','stroke-linecap':'round'});
    add('text',{x:tx,y:ty,'font-family':'Bahnschrift,Arial,sans-serif','font-size':'29','font-weight':'700',fill:'#14232b'}).textContent='KENTUCKY';
    add('text',{x:tx,y:ty+27,'font-family':'Bahnschrift,Arial,sans-serif','font-size':'18',fill:'#14232b'}).textContent='LOUISVILLE / RUN50 01 #3';
  });
  await page.locator('#map-slot').screenshot({path:'assets/wechat-run50-map-louisville-2024-editorial.png'});
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});

