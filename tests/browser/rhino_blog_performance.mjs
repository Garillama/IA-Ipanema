// Source-bound local projections, not a Tiendanube Twig renderer or a store performance benchmark.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
const run=process.argv[2];
if(!run)throw Error('Uso: node tests/browser/rhino_blog_performance.mjs <run-con-browser-cases.json>');
const cases=JSON.parse(await fs.readFile(path.join(run,'browser-cases.json'),'utf8'));
const checks=[],records=[];
const check=(name,passed,details)=>checks.push({name,status:passed?'passed':'failed',details});
const images=new Map();
function markup(phase,scenario,placeholder=false){
 const flags=phase==='after'?scenario.flags:[false,false,false];
 return `<!doctype html><html lang="es"><head><meta charset="utf-8"><title>QA local de prioridad del blog</title><style>
 ${cases.native_css}
 body{margin:16px;font-family:Arial;color:#111;background:#fff}h1{font-size:24px}.grid{display:grid;gap:20px;grid-template-columns:repeat(3,minmax(0,1fr))}.blog-card-media{position:relative;aspect-ratio:16/9}.blog-card-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}@media(max-width:767px){.grid{grid-template-columns:1fr}}
 </style></head><body><main><h1>Artículos — fixture local</h1><div class="grid">${flags.map((priority,i)=>{
 const src=`/image-${placeholder?'placeholder':'cover'}-${i}.svg`;
 // These branches project image.tpl's already-verified priority/lazy rules.
 const attributes=priority?`src="${src}" srcset="${src} 640w, ${src} 1024w" fetchpriority="high"`:`data-srcset="${src} 640w, ${src} 1024w"`;
 return `<article><h2><a href="/article-${i}">Artículo de prueba ${i+1}</a></h2>${scenario.show_image?`<div class="blog-card-media"><img ${attributes} class="${priority?'image-priority-high':'lazyload'} blog-card-img fade-in" sizes="100vw" alt="Portada de prueba ${i+1}"></div>`:''}</article>`;
 }).join('')}</div></main></body></html>`;
}
const server=http.createServer((req,res)=>{
 if(req.method!=='GET'){res.writeHead(405);res.end();return;}
 const u=new URL(req.url,'http://localhost');
 if(u.pathname.startsWith('/image-')){images.set(u.pathname,(images.get(u.pathname)||0)+1);res.writeHead(200,{'Content-Type':'image/svg+xml','Cache-Control':'no-store'});res.end('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675"><rect width="1200" height="675" fill="#335577"/></svg>');return;}
 const [,phase,name,kind]=u.pathname.split('/');const scenario=cases.cases.find(x=>x.name===name);
 if(!scenario){res.writeHead(404);res.end();return;}
 res.writeHead(200,{'Content-Type':'text/html;charset=utf-8','Cache-Control':'no-store'});res.end(markup(phase,scenario,kind==='placeholder'));
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
Object.assign(process.env,{IPANEMA_PUBLIC_URL:origin,IPANEMA_RESOURCE_ORIGINS:origin,IPANEMA_EVIDENCE_DIR:path.resolve(run,'blog-priority-browser')});
let browser;
try{
 const{puppeteer}=await import('../../tools/browser_runtime.mjs');browser=await puppeteer.launch();
 const matrix=[];
 for(const phase of['before','after'])for(const width of[360,390,768,1024,1440,1920])for(const placeholder of[false,true])matrix.push({phase,width,placeholder,name:'normal'});
 for(const name of['page2','index_fragment','filtered_landing','images_disabled','other_template'])matrix.push({phase:'after',width:390,placeholder:false,name});
 for(const item of matrix){
  const context=await browser.createBrowserContext(),page=await context.newPage();await page.setViewport({width:item.width,height:900,deviceScaleFactor:1});await page.setJavaScriptEnabled(false);
  const cdp=await page.createCDPSession();await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});const requests=[];
  cdp.on('Network.requestWillBeSent',e=>requests.push({url:e.request.url,type:e.type,priority:e.request.initialPriority}));
  await page.goto(origin+`/${item.phase}/${item.name}/${item.placeholder?'placeholder':'cover'}`,{waitUntil:'load',timeout:10000});
  const state=await page.evaluate(()=>({imgs:[...document.images].map(e=>({src:e.getAttribute('src'),currentSrc:e.currentSrc,priority:e.getAttribute('fetchpriority'),lazy:e.classList.contains('lazyload'),opacity:getComputedStyle(e).opacity,naturalWidth:e.naturalWidth,complete:e.complete,alt:e.alt})),links:[...document.querySelectorAll('article a')].map(e=>e.getAttribute('href')),boxes:[...document.querySelectorAll('.blog-card-media')].map(e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height})),scrollHeight:document.documentElement.scrollHeight}));
  const selected=cases.cases.find(x=>x.name===item.name);const expected=item.phase==='after'&&selected.flags[0]&&selected.show_image?1:0;const imageRequests=requests.filter(x=>x.type==='Image');const label=[item.phase,item.name,item.width,item.placeholder?'placeholder':'cover'].join(':');
  check(label+':image-request-count',imageRequests.length===expected,{actual:imageRequests.length,expected});
  check(label+':no-external-network',requests.every(x=>new URL(x.url).origin===origin));
  check(label+':links-preserved',state.links.join(',')==='/article-0,/article-1,/article-2');
  if(expected){check(label+':visible-without-js',state.imgs[0].opacity==='1'&&state.imgs[0].naturalWidth>0&&state.imgs[0].complete,state.imgs[0]);check(label+':high-network-priority',imageRequests[0].priority==='High',imageRequests[0]);check(label+':others-stay-lazy',state.imgs.slice(1).every(e=>e.lazy&&e.naturalWidth===0&&e.src===null));}
  records.push({...item,state,requests:imageRequests.map(x=>({...x,url:new URL(x.url).pathname}))});await context.close();
 }
 for(const width of[360,390,768,1024,1440,1920])for(const placeholder of[false,true]){
  const a=records.find(x=>x.phase==='before'&&x.width===width&&x.placeholder===placeholder&&x.name==='normal');const b=records.find(x=>x.phase==='after'&&x.width===width&&x.placeholder===placeholder&&x.name==='normal');
  check(`geometry:${width}:${placeholder}`,JSON.stringify(a.state.boxes)===JSON.stringify(b.state.boxes)&&a.state.scrollHeight===b.state.scrollHeight);
 }
}catch(e){check('runner',false,String(e.message));}
finally{
 if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));
 const result={at:new Date().toISOString(),project:'rhino-performance',kind:'local_blog_priority_projection_qa',outcome:checks.every(c=>c.status==='passed')?'passed':'failed',checks,records,network:'loopback-only; no storefront/API requests',limitations:['Does not render full Twig/platform.','No JavaScript and source-bound projected attribute branches; demonstrates browser discovery/visibility/priority, not published LCP reduction.','Fixture SVG is not the merchant JPEG; no asset compression improvement asserted.']};
 await fs.writeFile(path.join(run,'browser-qa.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({outcome:result.outcome,checks:checks.length,records:records.length,failed:checks.filter(x=>x.status==='failed')}));if(result.outcome!=='passed')process.exitCode=1;
}
