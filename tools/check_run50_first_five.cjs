const {chromium}=require('playwright');
const fs=require('fs');
const slugs=['louisville-marathon','kentucky-derby-marathon-2021','cleveland-marathon','new-york-city-marathon','san-francisco-marathon'];
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const map=await browser.newPage({viewport:{width:1200,height:704},deviceScaleFactor:1.5});
 for(const name of ['kentucky','cleveland','new-york','san-francisco']){
  await map.goto('http://127.0.0.1:8768/tmp/'+name+'-review-map.html');
  await map.locator('#us-map-master').waitFor();await map.waitForTimeout(400);
  await map.locator('#map-slot').screenshot({path:'assets/run50-first-five-20261102/'+name+'-map.png'});
 }
 await map.close();const report=[];
 for(const slug of slugs){
  const page=await browser.newPage({viewport:{width:390,height:844}});const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>Object.defineProperty(navigator,'clipboard',{value:{write:async(items)=>{window.copiedHTML=await (await items[0].getType('text/html')).text()}}}));
  await page.goto('http://127.0.0.1:8768/run50/wechat/'+slug+'-modern-rail.html');
  await page.evaluate(async()=>{await Promise.all([...document.images].map(im=>{im.loading='eager';return im.decode().catch(()=>{})}))});
  const audit=await page.evaluate(()=>{
   const imgs=[...document.querySelectorAll('main img')];let run=0,max=0;
   for(const n of document.querySelector('main').children){if(n.matches('p')){run+=n.textContent.length;max=Math.max(max,run)}else run=0}
   return {broken:imgs.filter(i=>!i.naturalWidth).map(i=>i.src),overflow:document.documentElement.scrollWidth>innerWidth,photos:imgs.length,maxTextRun:max,mapBoxes:[...document.querySelectorAll('.location-poster img')].map(i=>({x:i.getBoundingClientRect().x,width:i.getBoundingClientRect().width})),tones:[...new Set([...document.querySelectorAll('[data-cn-tone]')].map(e=>e.dataset.cnTone))],chapters:[...document.querySelectorAll('.chapter h2')].map(e=>e.textContent)};
  });
  await page.locator('.chapter').first().scrollIntoViewIfNeeded();await page.screenshot({path:'tmp/'+slug+'-light.png'});
  await page.locator('[data-theme-choice="dark"]').click();
  await page.locator('.location-poster').scrollIntoViewIfNeeded();await page.screenshot({path:'tmp/'+slug+'-dark-map.png'});
  await page.locator('select[aria-label="图片复制方式"]').selectOption('links');
  await page.locator('select[aria-label="选择全文或分段复制"]').selectOption('1');
  await page.locator('#copy-wechat').click();await page.waitForFunction(()=>window.copiedHTML);
  const copy=await page.evaluate(()=>{const d=new DOMParser().parseFromString(window.copiedHTML,'text/html');const nums=[...d.querySelectorAll('p')].filter(e=>/^\d\d$/.test(e.textContent.trim()));return {numbers:nums.map(e=>({text:e.textContent,bg:e.style.backgroundColor,color:e.style.color})),accents:[...new Set([...d.querySelectorAll('strong')].map(e=>e.style.color))],underline:d.querySelectorAll('[style*="underline"]').length}});
  report.push({slug,...audit,copy,errors});
  if(audit.broken.length||audit.overflow||errors.length||audit.mapBoxes[0].width!==audit.mapBoxes[1].width)throw Error(JSON.stringify(report.at(-1)));
  await page.close();
 }
 fs.writeFileSync('tmp/run50-first-five-qa.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
})();
