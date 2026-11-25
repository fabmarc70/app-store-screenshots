// Rendu des 10 visuels finaux (après node render-phones.js) : node render-final.js -> versions/final-3d/*.png (RGB, 1320x2868)
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
const ids=['01-planning','02-bulletin','03-simulateur','04-rentabilite','05-vacations','06-gain','07-radar','08-missions','09-carriere','10-confidentiel'];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1320,height:2868}});
fs.mkdirSync('versions/final-3d',{recursive:true});
for(const id of ids){await p.goto('file://'+path.resolve('deck-3d.html')+'?s='+id);
 await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);
 const out=`versions/final-3d/${id}.png`;await p.screenshot({path:out});
 execFileSync('python3',['-c',`from PIL import Image;Image.open('${out}').convert('RGB').save('${out}')`]);console.log('ok',id);}
await b.close();})();
