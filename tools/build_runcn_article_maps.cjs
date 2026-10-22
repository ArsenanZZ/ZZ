/* All RunCN article maps: shared Liupanshui styling and station-specific history. */
const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:860},deviceScaleFactor:1.5});
 const timeline=JSON.parse(fs.readFileSync(path.join(root,'tools/data/runcn-map-timeline.json'),'utf8'));
 const out=path.join(root,'assets/runcn-article-maps-20261022');fs.mkdirSync(out,{recursive:true});
 const makeEmblem=require('./runcn-map-emblems.cjs');
 const results=[];
 const geo=fs.readFileSync(path.join(root,'run50/china-map-svg.js'),'utf8');
 for(const cfg of timeline.pages){
 if(process.argv[2]&&process.argv[2]!==cfg.slug)continue;
 const completed=timeline.stations.filter(x=>x.station<=cfg.station);
 const provinces=Object.fromEntries([...new Set(completed.map(x=>x.province))].map(k=>[k,timeline.provinces[k]]));
 const dots=[...new Map(completed.map(x=>[x.city,[x.city,x.province,x.lat,x.lon]])).values()];
 const provinceBlock=JSON.stringify(provinces),dotBlock=JSON.stringify(dots);
 await page.goto('about:blank'); // Reset the SVG module scope for each historical snapshot.
 await page.setContent('<html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}#map{width:1200px;height:860px}svg{display:block;width:1200px;height:860px;font-family:"Microsoft YaHei",sans-serif}</style></head><body><div id="map"></div></body></html>');
 await page.addScriptTag({content:geo+';window.mapSvg=CHINA_MAP_SVG;window.labels=_CN_LABELS;window.provinces='+provinceBlock+';window.cityDots='+dotBlock});
 const mime=cfg.emblem?.endsWith('.svg')?'image/svg+xml':'image/png';
 const emblem=cfg.emblem?'data:'+mime+';base64,'+fs.readFileSync(path.join(root,cfg.emblem)).toString('base64'):'data:image/svg+xml;base64,'+Buffer.from(makeEmblem(cfg.icon)).toString('base64');
 await page.evaluate(({emblem,cfg})=>{
  const slot=document.getElementById('map');slot.innerHTML=window.mapSvg;
  const svg=slot.querySelector('svg');svg.setAttribute('viewBox','0 0 800 575');svg.removeAttribute('style');
  const ns='http://www.w3.org/2000/svg';
  const add=(tag,attrs,text)=>{const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text)el.textContent=text;svg.appendChild(el);return el;};
  svg.querySelectorAll('text').forEach(x=>x.remove());
  svg.querySelectorAll('path[id^="bg_"]').forEach(x=>{x.setAttribute('fill','#f0ede4');x.setAttribute('stroke','#d9dbd1');x.setAttribute('stroke-width','.5');});
  svg.querySelectorAll('path[id^="cn_"]').forEach(x=>{
   const palette={'#ff6b4a':'#dba58b','#ffbe3c':'#dfc58d','#45af55':'#b1c5a7','#a65dd2':'#bbaecc','#36a6b5':'#94bac1'};const original=window.provinces[x.id]?.[1];x.style.fill=original?(palette[original]||original):'#e9e5d9';if(window.provinces[x.id]){const raw=window.provinces[x.id][1];const h=raw.replace('#','');if(h.length===6){const rgb=[0,2,4].map((v,i)=>Math.round(parseInt(h.slice(v,v+2),16)*.43+[242,237,222][i]*.57));x.style.fill='rgb('+rgb.join(',')+')';}}x.style.stroke='#89968f';x.style.strokeWidth='.65';
  });
  const gz=svg.querySelector('#'+cfg.province);gz.style.fill='#927329';gz.style.stroke='#927329';gz.style.strokeWidth='2';
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
   if(best)labels.push({id,name,...best,size:id===cfg.province?18:short==='xinjiang'?20:short==='ningxia'?13:16});
  }
  // Keep the current province name inside its own shape and clear of the star.
  const active=labels.find(l=>l.id===cfg.province);
  if(active){
   const shape=svg.querySelector('#'+cfg.province),sx=(cfg.lon-70)*11.8,sy=(55-cfg.lat)*15;
   const box=shape.getBBox();let best=null,score=-Infinity;
   for(let yy=box.y+6;yy<box.y+box.height-6;yy+=2)for(let xx=box.x+12;xx<box.x+box.width-12;xx+=2){
    if(![-13,0,13].every(dx=>[-6,0,6].every(dy=>shape.isPointInFill(new DOMPoint(xx+dx,yy+dy)))))continue;
    const distance=Math.hypot(xx-sx,yy-sy);if(distance<24)continue;
    const value=-Math.hypot(xx-active.x,yy-active.y);if(value>score){score=value;best={x:xx,y:yy};}
   }
   if(best)Object.assign(active,best);
   else if(Math.hypot(active.x-sx,active.y-sy)<26){active.x=sx+42;active.y=sy+18;active.external=true;active.size=16;}

  }
  window.provinceLabels=labels;
  add('text',{x:35,y:40,'font-size':22,'font-family':'Noto Serif SC, SimSun, serif','font-weight':'800',fill:'#163e47'},'RunCN · '+(names[cfg.province.slice(3)]===cfg.city?'':names[cfg.province.slice(3)])+cfg.city);
  add('text',{x:35,y:65,'font-size':11,fill:'#365e66'},(cfg.date?cfg.date+' · ':'')+'第'+cfg.range+'站'+(cfg.station<10?' · 累计至本篇最后一站':''));
  window.cityDots.forEach(([city,,lat,lon])=>{if(city!==cfg.city)add('circle',{cx:(lon-70)*11.8,cy:(55-lat)*15,r:2.8,fill:'#ba6b50',stroke:'#fff8e8','stroke-width':.9});});
  const tx=(cfg.lon-70)*11.8,ty=(55-cfg.lat)*15;
  add('path',{d:`M 170 505 C 245 520 ${tx-75} ${ty+65} ${tx-10} ${ty+8}`,fill:'none',stroke:'#a34723','stroke-width':2.1});
  if(active?.external)add('path',{d:`M${tx+12} ${ty+5}L${active.x-18} ${active.y}`,fill:'none',stroke:'#927329','stroke-width':.8});
  window.provinceLabels.forEach(({id,name,x,y,size,external})=>add('text',{x,y,'font-size':size,'dominant-baseline':'middle','font-family':id===cfg.province?'Noto Serif SC, SimSun, serif':'KaiTi, STKaiti, serif','font-weight':id===cfg.province?'800':'600','text-anchor':'middle',fill:external?'#927329':id===cfg.province?'#fff6df':window.provinces[id]?'#344d54':'#87918b','paint-order':'stroke',stroke:external?'#f5f0e4':id===cfg.province?'#927329':'#f5f0e4','stroke-width':id===cfg.province?1:.8},name));
  // Small coastal municipalities use an uncluttered external label column.
  const external=[['北京',116.4,39.9,669,254],['天津',117.2,39.1,690,280],['上海',121.47,31.23,693,378],['香港',114.17,22.3,647,508],['澳门',113.54,22.2,647,533]];
  external.forEach(([name,lon,lat,tx,ty])=>{const px=(lon-70)*11.8,py=(55-lat)*15;add('path',{d:`M${px} ${py} L${tx-18} ${ty} L${tx-5} ${ty}`,fill:'none',stroke:'#8e9a95','stroke-width':.75});add('text',{x:tx,y:ty,'dominant-baseline':'middle','font-size':14,'font-family':'KaiTi, STKaiti, serif',fill:name===cfg.city?'#927329':'#536a71','font-weight':name===cfg.city?'800':'500'},name);});
  // Existing site projection: x=(lon-70)*11.8, y=(55-lat)*15.
  const x=(cfg.lon-70)*11.8,y=(55-cfg.lat)*15;
  add('circle',{cx:x,cy:y,r:13,fill:'#fff4b3',opacity:.7});
  const points=Array.from({length:10},(_,i)=>{const a=-Math.PI/2+i*Math.PI/5,r=i%2?4.5:10;return (x+Math.cos(a)*r)+','+(y+Math.sin(a)*r)}).join(' ');
  add('polygon',{points,fill:'#e95532',stroke:'#fffdf0','stroke-width':1.8});

  add('image',{href:emblem,x:30,y:414,width:220,height:140});
  add('text',{x:140,y:565,'text-anchor':'middle','font-size':24,'font-family':'Noto Serif SC, SimSun, serif','font-weight':'800',fill:'#173d48'},cfg.city);
 },{emblem,cfg});
 await page.evaluate(()=>document.fonts.ready);
 await page.locator('#map').screenshot({path:path.join(out,cfg.slug+'.jpg')});
 const report=await page.evaluate(()=>({labels:window.provinceLabels.length,filled:[...document.querySelectorAll('path[id^="cn_"]')].filter(p=>p.style.fill&&p.style.fill!=='rgb(233, 229, 217)').map(p=>p.id)}));
 if(JSON.stringify([...report.filled].sort())!==JSON.stringify(Object.keys(provinces).sort()))throw new Error('Historical fill mismatch: '+cfg.slug);
 results.push({slug:cfg.slug,station:cfg.station,provinces:Object.keys(provinces),cities:dots.map(x=>x[0]),...report});
 console.log(cfg.slug,Object.keys(provinces).length,'provinces',dots.length,'cities');
 }
 fs.mkdirSync(path.join(root,'tmp'),{recursive:true});fs.writeFileSync(path.join(root,'tmp/runcn-map-audit.json'),JSON.stringify(results,null,2));
 await browser.close();
})();
