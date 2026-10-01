// Render the established Run50 SVG with an editorial city callout.
// Usage: NODE_PATH=<playwright packages> node tools/build_wechat_michigan_editorial_map.cjs
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({channel:'chrome', headless:true});
  const page = await browser.newPage({viewport:{width:1200,height:704},deviceScaleFactor:1.5});
  await page.goto('file:///' + path.resolve('tmp/wechat-blue-ridge-editorial-map.html').replaceAll('\\','/'));
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
    // The feather tip lands beside the Roanoke star; the title sits offshore.
    const feather=add('svg',{x:cx+5,y:cy+5,width:88,height:70,viewBox:'0 0 920 727',overflow:'hidden'});
    add('image',{href:'../assets/blue-ridge-map-callout-feather.png',width:2164,height:727},feather);
    add('path',{d:`M ${cx+82} ${cy+63} C ${cx+150} ${cy+112} ${cx+96} ${cy+205} ${cx+178} ${cy+237}`,fill:'none',stroke:'#b58230','stroke-width':'2.6'});
    const title=add('svg',{x:cx+170,y:cy+190,width:265,height:100,viewBox:'920 180 1244 470',overflow:'hidden'});
    add('image',{href:'../assets/blue-ridge-map-callout-feather.png',width:2164,height:727},title);




  });
  await page.waitForTimeout(500);
  await page.locator('#map-slot').screenshot({path:'assets/wechat-run50-map-blue-ridge-24-editorial.png'});
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});

