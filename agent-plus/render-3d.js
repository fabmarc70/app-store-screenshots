// Rendu des exemples inclinés : node render-3d.js -> versions/exemples-3d
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1320,height:2868}});
fs.mkdirSync('versions/exemples-3d',{recursive:true});
for(const id of ['e1','e2','e3','e4']){await p.goto('file://'+path.resolve('deck-3d.html')+'?s='+id);
 await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:`versions/exemples-3d/${id}.png`});}
await b.close();})();
