// Real Chrome, offline: existing motion script and archived public card markup.
// Does not render Twig, contact the store or submit forms.
import fs from 'node:fs/promises';
import path from 'node:path';
const run=path.resolve(process.argv[2]),theme=path.resolve(process.argv[3]);
process.env.IPANEMA_EVIDENCE_DIR=path.join(run,'browser');process.env.IPANEMA_ALLOW_NETWORK='0';
delete process.env.IPANEMA_AUDIT_PASSWORD;
const {puppeteer}=await import('../../tools/browser_runtime.mjs');
const scriptBefore=await fs.readFile(path.join(run,'before/static/js/damar-motion.js'),'utf8');
const scriptAfter=await fs.readFile(path.join(theme,'static/js/damar-motion.js'),'utf8');
const css=await fs.readFile(path.join(theme,'static/css/damar.css'),'utf8');
const archived=await fs.readFile(new URL('../runs/damarbeauty/20261108T211919-initial-audit-b5d2317b/public-home-initial.html',import.meta.url),'utf8');
const checks=[];const browser=await puppeteer.launch();
const assert=(name,pass,details)=>{checks.push({name,passed:!!pass,details});};
async function pageWith(html,width=390){
 const page=await browser.newPage(),cdp=await page.createCDPSession();
 await cdp.send('Network.enable');await cdp.send('Network.setBlockedURLs',{urls:['*']});
 await page.setViewport({width,height:900,deviceScaleFactor:1});
 await page.setContent(`<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; connect-src 'none'"><title>Offline usability fixture</title><style>${css}</style></head><body>${html}</body></html>`);
 return {page,cdp};
}
try{
 const sections='<main>'+[0,820,1100,1400,1700,2000].map((top,i)=>`<section id="section-${i}" data-section-id="${i}" style="position:absolute;top:${top}px;height:150px;width:300px;background:white;color:black">Sección ${i}</section>`).join('')+'</main>';
 for(const width of [360,390,768,1024,1440,1920]){
  const states=[];
  for(const [version,script] of [['before',scriptBefore],['after',scriptAfter]]){
   const {page}=await pageWith(sections,width);
   try{
    await page.addScriptTag({content:script});
    states.push(await page.evaluate(()=>({partially_visible_pending:document.getElementById('section-1').classList.contains('damar-motion-pending'),initially_visible:!document.getElementById('section-0').classList.contains('damar-motion-pending'),pending:[...document.querySelectorAll('.damar-motion-pending')].map(e=>e.id)})));
    if(width===390)await page.screenshot({path:path.join(run,'browser',`motion-${version}.png`)});
   }finally{await page.close();}
  }
  assert(`motion-visible-${width}`,states[0].partially_visible_pending&&!states[1].partially_visible_pending&&states[1].initially_visible,{before:states[0],after:states[1]});
  assert(`motion-bounded-${width}`,states[1].pending.length===3,states[1].pending);
 }
 for(const mode of ['reduced-motion','no-observer']){
  const {page}=await pageWith(sections);
  try{
   if(mode==='reduced-motion')await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
   else await page.evaluate(()=>{window.IntersectionObserver=undefined;});
   await page.addScriptTag({content:scriptAfter});
   assert(mode,await page.evaluate(()=>!document.querySelector('.damar-motion-pending')));
  }finally{await page.close();}
 }
 const {page,cdp}=await pageWith('<main id="cards"></main>');
 try{
  const samples=await page.evaluate(html=>{
   const d=new DOMParser().parseFromString(html,'text/html');
   const selected=[d.querySelector('a.product-item-link'),d.querySelector('a.damar-home-product-compact'),d.querySelector('a.damar-home-routine__link'),[...d.querySelectorAll('a.product-item-quick-shop-modal-trigger')].find(e=>e.textContent.includes('Ver producto'))];
   if(selected.some(e=>!e))throw Error('Archived card consumers missing.');
   return selected.map((e,i)=>{e.id='sample-'+i;for(const n of e.querySelectorAll('[src],[srcset]')){n.removeAttribute('src');n.removeAttribute('srcset');}return e.outerHTML;});
  },archived);
  await page.evaluate(samples=>{document.getElementById('cards').innerHTML=samples.join('');},samples);
  for(let i=0;i<4;i++){
   const selector='#sample-'+i;
   const before=await page.$eval(selector,e=>({href:e.getAttribute('href'),text:e.textContent}));
   await page.$eval(selector,(e,i)=>{if(i===3)e.setAttribute('aria-label',e.getAttribute('aria-label').replace(/^Ver /,'Ver producto: '));else e.removeAttribute('aria-label');},i);
   const after=await page.$eval(selector,e=>({href:e.getAttribute('href'),text:e.textContent,label:(e.querySelector('.product-item-name,.damar-home-product-compact__name,strong')?.textContent||'Ver producto').trim()}));
   const doc=await cdp.send('DOM.getDocument'),node=await cdp.send('DOM.querySelector',{nodeId:doc.root.nodeId,selector});
   const ax=await cdp.send('Accessibility.getPartialAXTree',{nodeId:node.nodeId,fetchRelatives:false});
   const name=ax.nodes.find(n=>n.role?.value==='link')?.name?.value||'';
   const norm=s=>s.normalize('NFC').replace(/\s+/g,' ').trim().toLocaleLowerCase('es');
   assert(`card-name-${i}`,norm(name).includes(norm(after.label)),{visible:after.label,accessible:name});
   assert(`card-contract-${i}`,before.href===after.href&&before.text===after.text);
  }
 }finally{await page.close();}
}finally{
 await browser.close();await fs.writeFile(path.join(run,'browser','usability.json'),JSON.stringify({method:'Chrome offline; actual motion scripts, archived card markup transformed to match local label changes. Remote resources blocked. Not platform Twig rendering.',checks},null,2));
}
console.log(JSON.stringify({checks:checks.length,passed:checks.filter(c=>c.passed).length}));
if(checks.some(c=>!c.passed))process.exitCode=1;
