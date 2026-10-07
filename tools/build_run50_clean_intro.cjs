const {chromium}=require('playwright');
const fs=require('fs');const {execFileSync}=require('child_process');
(async()=>{
 const out='tmp/run50-clean-frames';fs.mkdirSync(out,{recursive:true});
 const shapes=`<path d="M97 18v-8l9 8v-8l9 8v-8l9 10 M83 23h52v51H83z"/><circle cx="119" cy="40" r="5" fill="#3262bc"/><path d="M110 81h-14c-7 0-9 6-9 12s4 10 11 10h38V69c-9-6-7-19 2-19s13 10 6 16v45h-49c-19 0-19-27-3-27 M88 85H55v29c-9 4-8 17 1 18s13-12 6-17V94h20 M100 111v34H77v-11H55v18h50v-15h16v23h17v10h-29v-23 M81 151v30H61v18H50v-33h20v-15"/>`;
 const speed=`<path d="M66 58H28 M66 70H44 M46 139H29 M48 151H18"/>`;
 const baseSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="280" height="300" viewBox="0 0 224 240"><g transform="translate(18 8)"><g id="runner" fill="none" stroke-linecap="round" stroke-linejoin="round"><g stroke="#f5cf57" stroke-width="8">${shapes}</g><g stroke="#3262bc" stroke-width="4">${shapes}</g></g><g id="wind" fill="none" stroke-linecap="round"><g stroke="#f5cf57" stroke-width="8">${speed}</g><g stroke="#3262bc" stroke-width="4">${speed}</g></g></g><text id="word" x="112" y="236" text-anchor="middle" font-family="Arial, sans-serif" font-size="32" font-weight="900" letter-spacing="-1.3" fill="#3262bc" stroke="#f5cf57" stroke-width="2.2" paint-order="stroke">Run50</text></svg>`;

 const b=await chromium.launch({channel:'msedge',headless:true});const p=await b.newPage({viewport:{width:280,height:300},deviceScaleFactor:1});
 for(const theme of ['light','dark']) {
 const svg=baseSvg.replace(/<g stroke="#f5cf57" stroke-width="8">[\s\S]*?<\/g>/g,'').replace('stroke="#f5cf57" stroke-width="2.2"','stroke="none"').replaceAll('#3262bc',theme==='dark'?'#f6c62e':'#3262bc');
 fs.writeFileSync(`assets/run50-intro-${theme}.svg`,svg);
 await p.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block}</style>${svg}`);
 for(let i=0;i<60;i++){
  await p.evaluate(t=>{let a=Math.min(1,t/.4),w=Math.max(0,Math.min(1,(t-.55)/.35)),z=Math.max(0,Math.min(1,(t-1.05)/.4));document.querySelector('#runner').style.opacity=a;document.querySelector('#wind').style.opacity=w;document.querySelector('#wind').style.transform=`translateX(${(1-w)*-10}px)`;document.querySelector('#word').style.opacity=z;},i/15);
  await p.screenshot({path:`${out}/${String(i).padStart(3,'0')}.png`,omitBackground:true});
 }
 await p.screenshot({path:`assets/run50-intro-${theme}-still.png`,omitBackground:true});
 execFileSync('ffmpeg',['-y','-loglevel','error','-framerate','15','-i',out+'/%03d.png','-filter_complex','split[a][b];[a]palettegen=reserve_transparent=1[p];[b][p]paletteuse=alpha_threshold=128:dither=sierra2_4a','-loop','0',`assets/run50-intro-${theme}.gif`]);
 }
 await b.close();
 console.log('Transparent runner → wind → Run50 intro rendered');
})().catch(e=>{console.error(e);process.exit(1)});
