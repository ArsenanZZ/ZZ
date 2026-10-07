const {chromium}=require('playwright');
const fs=require('fs');const {execFileSync}=require('child_process');
const data=p=>'data:image/png;base64,'+fs.readFileSync(p).toString('base64');
(async()=>{
const out='tmp/run50-cutout-frames';fs.mkdirSync(out,{recursive:true});
const robot=data('assets/run50-robot-cutout-20261007-v2.png');
const word=data('assets/run50-wordmark-road-20261007.png');
const b=await chromium.launch({channel:'msedge',headless:true});const p=await b.newPage({viewport:{width:280,height:350}});
for(const theme of ['light','dark']){
const color=theme==='dark'?'#f6c62e':'#3262bc';
const rects='<rect x="210" y="355" width="294" height="146"/><rect x="210" y="839" width="294" height="131"/>';
const art=`<svg xmlns="http://www.w3.org/2000/svg" width="280" height="350" viewBox="0 0 280 350"><defs><filter id="ink" color-interpolation-filters="sRGB"><feComponentTransfer in="SourceAlpha" result="cleanAlpha"><feFuncA type="discrete" tableValues="0 0 0 0 0 0 0 1"/></feComponentTransfer><feFlood flood-color="${color}"/><feComposite operator="in" in2="cleanAlpha"/></filter></defs><svg width="280" height="280" viewBox="0 0 1280 1280"><defs><mask id="body"><rect width="1280" height="1280" fill="white"/><g fill="black">${rects}</g></mask><mask id="lines"><g fill="white">${rects}</g></mask></defs><image id="runner" href="${robot}" width="1280" height="1280" filter="url(#ink)" mask="url(#body)"/><image id="wind" href="${robot}" width="1280" height="1280" filter="url(#ink)" mask="url(#lines)"/></svg><image id="word" href="${word}" x="0" y="260" width="280" height="94" filter="url(#ink)"/></svg>`;
await p.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block}</style>${art}`);
for(let i=0;i<60;i++){
await p.evaluate(t=>{document.querySelector('#runner').style.opacity=Math.min(1,t/.4);document.querySelector('#wind').style.opacity=Math.max(0,Math.min(1,(t-.55)/.3));document.querySelector('#word').style.opacity=Math.max(0,Math.min(1,(t-1)/.4));},i/15);
await p.screenshot({path:`${out}/${String(i).padStart(3,'0')}.png`,omitBackground:true});}
await p.screenshot({path:`assets/run50-cutout-intro-${theme}-still.png`,omitBackground:true});
execFileSync('ffmpeg',['-y','-loglevel','error','-framerate','15','-i',out+'/%03d.png','-filter_complex','split[a][b];[a]palettegen=reserve_transparent=1[p];[b][p]paletteuse=alpha_threshold=128:dither=sierra2_4a','-loop','0',`assets/run50-cutout-intro-${theme}.gif`]);
}
await b.close();console.log('Original cutout and approved wordmark GIFs complete');
})().catch(e=>{console.error(e);process.exit(1)});

