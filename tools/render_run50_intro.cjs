const {chromium}=require('playwright');
const fs=require('fs');const path=require('path');
(async()=>{const output=process.argv[2];if(!output)throw Error('Pass an output frames directory');fs.mkdirSync(output,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:720,height:480},deviceScaleFactor:1});
await page.goto(process.argv[3] || 'http://127.0.0.1:8765/tools/run50-intro/index.html');
await page.waitForFunction(()=>Boolean(window.__timelines?.['run50-intro']));await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
for(let i=0;i<100;i++){await page.evaluate(t=>{window.__timelines['run50-intro'].seek(t);},i/20);await page.screenshot({path:path.join(output,`frame-${String(i).padStart(3,'0')}.png`),omitBackground:true});}
await page.evaluate(()=>{window.__timelines['run50-intro'].seek(2.5);});await page.screenshot({path:'assets/run50-robot-intro-still.png',omitBackground:true});await browser.close();})();
