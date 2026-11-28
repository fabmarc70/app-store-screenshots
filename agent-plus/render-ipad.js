// Rendu des 3 visuels iPad 13" (après python3 ipad_screens.py + node render-phones.js) -> versions/ipad/*.png (RGB 2064x2752)
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2064,height:2752}});
fs.mkdirSync('versions/ipad',{recursive:true});
for(const id of ['01-planning','02-bulletin','03-simulateur']){await p.goto('file://'+path.resolve('deck-ipad.html')+'?s='+id);
 await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);
 const out=`versions/ipad/${id}.png`;await p.screenshot({path:out});
 execFileSync('python3',['-c',`from PIL import Image;Image.open('${out}').convert('RGB').save('${out}')`]);console.log('ok',id);}
await b.close();})();
