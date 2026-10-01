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
    // Keep the callout in the open water below the map labels.
    add('image',{href:'../assets/louisiana-map-callout-jazz.png',x:cx-55,y:cy+125,width:350,height:118});
    const gold=add('linearGradient',{id:'pointer-gold',x1:'0%',y1:'0%',x2:'0%',y2:'100%'},defs);
    add('stop',{offset:'0%','stop-color':'#e4bc65'},gold);
    add('stop',{offset:'60%','stop-color':'#b58230'},gold);
    add('stop',{offset:'100%','stop-color':'#85551f'},gold);
    const marker=add('marker',{id:'louisiana-pointer',viewBox:'0 0 32 28',refX:'29',refY:'14',markerWidth:'13',markerHeight:'12',orient:'auto',overflow:'visible'},defs);
    // Curved split feather: a calligraphic arrowhead with open breathing room.
    add('path',{d:'M 2 2 C 12 3 18 10 30 14 C 19 13 9 9 2 2 Z',fill:'url(#pointer-gold)',stroke:'#946628','stroke-width':'.65'},marker);
    add('path',{d:'M 2 26 C 10 24 19 17 30 14 C 18 15 10 18 2 26 Z',fill:'url(#pointer-gold)',stroke:'#946628','stroke-width':'.65'},marker);
    add('path',{d:'M 7 14 Q 20 14 30 14',fill:'none',stroke:'#a87827','stroke-width':'1.4','stroke-linecap':'round'},marker);
    add('path',{d:`M ${cx-33} ${cy+180} C ${cx-68} ${cy+191} ${cx-67} ${cy+163} ${cx-48} ${cy+171}`,fill:'none',stroke:'#b58230','stroke-width':'2.3','stroke-linecap':'round'});
    add('path',{d:`M ${cx-33} ${cy+180} C ${cx-125} ${cy+158} ${cx-142} ${cy+66} ${cx-9} ${cy+8}`,fill:'none',stroke:'url(#pointer-gold)','stroke-width':'3.4','stroke-linecap':'round','marker-end':'url(#louisiana-pointer)'});


  });
  await page.waitForTimeout(500);
  await page.locator('#map-slot').screenshot({path:'assets/wechat-run50-map-louisiana-23-editorial.png'});
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});

