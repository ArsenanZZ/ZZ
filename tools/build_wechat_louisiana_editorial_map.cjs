// Render the established Run50 SVG with an editorial city callout.
// Usage: NODE_PATH=<playwright packages> node tools/build_wechat_michigan_editorial_map.cjs
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({channel:'chrome', headless:true});
  const page = await browser.newPage({viewport:{width:1200,height:704},deviceScaleFactor:1.5});
  await page.goto('file:///' + path.resolve('tmp/wechat-louisiana-editorial-map.html').replaceAll('\\','/'));
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
    add('image',{href:'../assets/louisiana-map-callout-jazz.png',x:680,y:78,width:390,height:131});
    add('text',{x:cx+55,y:cy+93,'font-family':'Georgia,serif','font-size':'24',fill:'#aa823a'}).textContent='♪';
    add('path',{d:`M ${cx+60} ${cy+76} Q ${cx+50} ${cy+40} ${cx+10} ${cy+12}`,fill:'none',stroke:'#aa823a','stroke-width':'1.5','stroke-linecap':'round',opacity:'.85'});

  });
  await page.waitForTimeout(500);
  await page.locator('#map-slot').screenshot({path:'assets/wechat-run50-map-louisiana-23-editorial.png'});
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});

