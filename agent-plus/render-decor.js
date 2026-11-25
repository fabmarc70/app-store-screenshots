// Rendu des objets 3D décoratifs en PNG transparents : node render-decor.js -> decor/png/<nom>.png
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const TYPES={'.html':'text/html','.js':'text/javascript','.json':'application/json','.otf':'font/otf','.png':'image/png'};
const server=http.createServer((req,res)=>{const f=path.join(__dirname,decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':TYPES[path.extname(f)]||'application/octet-stream'});res.end(d);});});
const NAMES=process.argv.slice(2).length?process.argv.slice(2):['coin','calendar','shield','lock','pin','plus','document','briefcase','bell','magnifier'];
server.listen(0,async()=>{const port=server.address().port;
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const p=await b.newPage({viewport:{width:900,height:900}});
  p.on('console',m=>{if(m.type()==='error')console.log('console:',m.text())});p.on('pageerror',e=>console.log('pageerror:',e.message));
  for(const n of NAMES){await p.goto(`http://localhost:${port}/decor/objects.html?o=${n}&size=900`);
    await p.waitForFunction(()=>window.__done,null,{timeout:60000});
    await p.screenshot({path:`decor/png/${n}.png`,omitBackground:true});console.log('ok',n);}
  await b.close();server.close();});
