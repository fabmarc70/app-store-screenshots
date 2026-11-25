// Rendu des visuels v2 : node render-v2.js  -> versions/bleu, versions/clair
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const ids=['planning','bulletin','simulateur','rentabilite','vacations','gain','radar','missions','carriere','confidentiel'];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1320,height:2868}});
for(const t of ['bleu','clair']){fs.mkdirSync(`versions/${t}`,{recursive:true});
 for(const [i,id] of ids.entries()){await p.goto('file://'+path.resolve('deck-v2.html')+`?s=${id}&t=${t}`);
  await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:`versions/${t}/${String(i+1).padStart(2,'0')}-${id}.png`});}}
await b.close();})();
