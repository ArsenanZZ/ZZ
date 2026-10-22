/* Compatibility entry point: all RunCN maps share one historical renderer. */
const {spawnSync}=require('child_process');
const path=require('path');
const r=spawnSync(process.execPath,[path.join(__dirname,'build_runcn_article_maps.cjs'),'qinghai-xining-marathon'],{stdio:'inherit'});
process.exit(r.status??1);
