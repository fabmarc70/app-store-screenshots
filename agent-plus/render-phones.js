// Rendu des téléphones 3D (three.js) en PNG transparents, recadrés au plus juste.
// Usage : node render-phones.js '<json [{name,img,ry,rx,rz,color}]>'  -> phone3d/out/<name>.png
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const TYPES={'.html':'text/html','.js':'text/javascript','.png':'image/png','.otf':'font/otf'};
const server=http.createServer((req,res)=>{const f=path.join(__dirname,decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':TYPES[path.extname(f)]||'application/octet-stream'});res.end(d);});});
const jobs=JSON.parse(process.argv[2]);
server.listen(0,async()=>{const port=server.address().port;
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const p=await b.newPage({viewport:{width:2400,height:3800}});
  p.on('pageerror',e=>console.log('pageerror:',e.message));
  for(const j of jobs){const qs=new URLSearchParams({img:j.img,ry:j.ry,rx:j.rx,rz:j.rz,color:j.color||'natural'});
    await p.goto(`http://localhost:${port}/phone3d/phone.html?${qs}`);
    await p.waitForFunction(()=>window.__done,null,{timeout:120000});
    const out=`phone3d/out/${j.name}.png`;await p.screenshot({path:out,omitBackground:true});
    execFileSync('python3',['-c',`from PIL import Image;im=Image.open('${out}');im.crop(im.getchannel('A').getbbox()).save('${out}')`]);
    console.log('ok',j.name);}
  await b.close();server.close();});
