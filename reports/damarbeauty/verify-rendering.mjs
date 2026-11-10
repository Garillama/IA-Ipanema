// Prueba de equivalencia en navegador: muta SOLO el DOM/CSS del navegador local.
// No publica ni envía formularios. Reutiliza runtime protegido y comparador V2.
import fs from 'node:fs/promises';
import path from 'node:path';
const output=path.resolve(process.argv[2]);
process.env.IPANEMA_PUBLIC_URL='https://damarbeauty.mx/';
process.env.IPANEMA_ALLOWED_ORIGINS='https://damarbeauty.mx';
process.env.IPANEMA_ALLOW_NETWORK='1';
process.env.IPANEMA_EVIDENCE_DIR=output;
delete process.env.IPANEMA_AUDIT_PASSWORD;
const {puppeteer}=await import('../../tools/browser_runtime.mjs');
const {createHash}=await import('node:crypto');
const hash=x=>createHash('sha256').update(JSON.stringify(x)).digest('hex');
const pages={home:'/',category:'/lo-mas-nuevo-lippies/',pdp:'/productos/r-h-o-d-e-peptide-lip-tint/'};
const records=[];const browser=await puppeteer.launch();
try{
 for(const [name,route] of Object.entries(pages))for(const width of [360,390,768,1024,1440,1920]){
  const context=await browser.createBrowserContext();
  try{
   const page=await context.newPage();await page.setViewport({width,height:900,deviceScaleFactor:1});
   await page.goto(new URL(route,'https://damarbeauty.mx').href,{waitUntil:'domcontentloaded',timeout:45000});
   await page.evaluate(()=>document.fonts.ready);
   await page.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'});
   await page.waitForNetworkIdle({idleTime:500,timeout:5000}).catch(()=>{});
   const measure=()=>page.evaluate(()=>({
    h1:[...document.querySelectorAll('h1')].map(e=>({text:e.textContent.trim(),visible:!!e.getClientRects().length})),
    nodes:[...document.querySelectorAll('header,main,footer,main h1,main h2,main h3,main img,main a,main button,main section')].map(e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);return [e.tagName,e.id,e.className,r.x,r.y,r.width,r.height,s.display,s.color,s.fontFamily,s.fontSize,s.fontWeight,s.lineHeight,s.padding,s.margin,s.gridTemplateColumns];
    }),overflow:document.documentElement.scrollWidth>innerWidth+1
   }));
   const before=await measure();await page.screenshot({path:path.join(output,`${name}-${width}-before.png`)});
   const applied=await page.evaluate(name=>{
    if(name==='home'){
     const hidden=document.querySelector('#logo h1[style]');
     if(!hidden||getComputedStyle(hidden).display!=='none')throw Error('No coincide H1 oculto del logo.');
     hidden.remove();return {removed_hidden_h1:true,disabled_styles:0};
    }
    const sheet=[...document.querySelectorAll('link[rel=stylesheet]')].find(e=>/\/damar-home-content-[^/]+\.min\.css/.test(e.href));
    if(!sheet)throw Error('No se encontró stylesheet esperado.');sheet.disabled=true;
    return {removed_hidden_h1:false,disabled_styles:1};
   },name);
   await new Promise(r=>setTimeout(r,120));const after=await measure();await page.screenshot({path:path.join(output,`${name}-${width}-after.png`)});
   records.push({page:name,width,applied,geometry_before:hash(before.nodes),geometry_after:hash(after.nodes),geometry_equal:hash(before.nodes)===hash(after.nodes),h1_before:before.h1,h1_after:after.h1,overflow_before:before.overflow,overflow_after:after.overflow});
  }finally{await context.close();}
 }
}finally{
 await browser.close();await fs.writeFile(path.join(output,'render-comparison.json'),JSON.stringify({at:new Date().toISOString(),method:'DOM/CSS simulation of scoped source changes, viewport screenshots; not Twig rendering or production deployment',records},null,2));
}
console.log(JSON.stringify({cases:records.length,geometry_equal:records.filter(r=>r.geometry_equal).length}));
