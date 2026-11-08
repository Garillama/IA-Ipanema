#!/usr/bin/env node
import fs from 'node:fs/promises';
import {puppeteer,authenticate,cliRequire,evidenceRoot,projectUrl,pageUrl} from './browser_runtime.mjs';
const home=projectUrl();
const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
const result={verifiedAt:new Date().toISOString(),states:[],overflow:[],media:[],limitations:['Prueba sin transacciones: no agrega productos, aplica cupones, envía contacto/newsletter ni crea cuentas.','Lectura de foco automatizada, sin lector de pantalla humano.']};
try{
 const cookies=await authenticate(browser,home+'?exit_preview_theme_installation');const context=await browser.createBrowserContext();await context.setCookie(...cookies);const p=await context.newPage();
 const snapshot=async(selector)=>await p.evaluate(selector=>{const e=document.querySelector(selector);const a=document.activeElement;return {exists:!!e,display:e?getComputedStyle(e).display:null,role:e?.getAttribute('role'),ariaModal:e?.getAttribute('aria-modal'),label:e?.getAttribute('aria-label'),labelledby:e?.getAttribute('aria-labelledby'),text:e?.innerText.slice(0,1600),active:{tag:a?.tagName,id:a?.id,class:typeof a?.className==='string'?a.className:'',label:a?.getAttribute('aria-label')},focusInside:!!e?.contains(a)};},selector);
 const settle=async(selector)=>await p.evaluate(async selector=>{const e=document.querySelector(selector);if(!e)return;const animations=e.getAnimations({subtree:true}).filter(a=>a.effect?.getComputedTiming().iterations!==Infinity);await Promise.race([Promise.all(animations.map(a=>a.finished.catch(()=>{}))),new Promise(r=>setTimeout(r,800))]);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));},selector);
 await p.setViewport({width:390,height:900,isMobile:true,hasTouch:true});await p.goto(home,{waitUntil:'networkidle2'});
 for(const [name,trigger,target] of [['menu','button[data-target="#nav-hamburger"]','#nav-hamburger'],['cart-empty','button[data-target="#modal-cart"]','#modal-cart']]){
  const el=await p.$(trigger);if(!el){result.states.push({name,unavailable:true});continue;}
  await el.click();
  try{await p.waitForFunction(s=>getComputedStyle(document.querySelector(s)).display!=='none',{timeout:4000},target);}catch(e){
   result.states.push({name,target,status:'No se abrió con el clic automatizado en esta ejecución',snapshot:await snapshot(target),url:p.url()});
   await p.screenshot({path:`${evidenceRoot}/screenshots/state-${name}-not-open-390.png`});
   await p.goto(home,{waitUntil:'networkidle2'});continue;
  }
  await settle(target);const opened=await snapshot(target);await p.addScriptTag({path:cliRequire.resolve('axe-core')});
  const axe=await p.evaluate(async(selector)=>{const r=await window.axe.run(document.querySelector(selector),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {violations:r.violations,incomplete:r.incomplete};},target);
  const focusPath=[];for(let i=0;i<6;i++){await p.keyboard.press('Tab');focusPath.push(await snapshot(target));}
  await p.screenshot({path:`${evidenceRoot}/screenshots/state-${name}-390.png`});await p.keyboard.press('Escape');await settle(target);
  const closedByEscape=await snapshot(target);
  if(closedByEscape.display!=='none'){
   const close=await p.$(`${target} .js-modal-close-private`);if(close)await close.click();
  }
  result.states.push({name,opened,focusPath,closedByEscape,axe});
 }
 const search=await p.$('.js-search-trigger');if(search){await search.click();result.states.push({name:'search-expanded',state:await snapshot('.js-search-form')});await p.keyboard.press('Escape');}
 for(const width of [768,1024]){
  await p.setViewport({width,height:900,isMobile:false,hasTouch:false});await p.goto(home,{waitUntil:'networkidle2'});
  result.overflow.push(await p.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,candidates:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();if(!r.width||r.right<=innerWidth+1&&r.left>=-1)return false;let a=e.parentElement;while(a&&a!==document.body){const s=getComputedStyle(a);if(['hidden','clip','auto','scroll'].includes(s.overflowX))return false;a=a.parentElement;}return getComputedStyle(e).position!=='fixed';}).slice(0,20).map(e=>({tag:e.tagName,id:e.id,class:typeof e.className==='string'?e.className:'svg',rect:{left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,width:e.getBoundingClientRect().width}}))})));
  await p.screenshot({path:`${evidenceRoot}/screenshots/state-overflow-${width}.png`});
 }
 for(const [name,url] of [['home',home],['category',pageUrl('category')],['pdp',pageUrl('pdp')]]){
  await p.setViewport({width:390,height:900,isMobile:true,hasTouch:true});await p.goto(url,{waitUntil:'networkidle2'});
  const network=[];const responseHandler=res=>{if(res.request().resourceType()==='image')network.push({url:res.url(),status:res.status()});};p.on('response',responseHandler);
  const before=await p.evaluate(()=>({images:document.images.length,loaded:[...document.images].filter(e=>e.naturalWidth>1).length,duplicates:document.querySelectorAll('.swiper-slide-duplicate').length}));
  const height=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<height;y+=800){await p.evaluate(y=>scrollTo(0,y),y);await new Promise(r=>setTimeout(r,80));}
  await p.waitForNetworkIdle({idleTime:500,timeout:7000}).catch(()=>{});
  const after=await p.evaluate(()=>({images:[...document.images].map(e=>({src:e.currentSrc,loading:e.loading,fetchPriority:e.fetchPriority,naturalWidth:e.naturalWidth,width:e.width,height:e.height,visible:e.getClientRects().length>0})),duplicates:document.querySelectorAll('.swiper-slide-duplicate').length,duplicateIds:Object.entries([...document.querySelectorAll('[id]')].reduce((o,e)=>(o[e.id]=(o[e.id]||0)+1,o),{})).filter(([,n])=>n>1)}));p.off('response',responseHandler);
  await p.screenshot({path:`${evidenceRoot}/screenshots/state-${name}-scrolled-390.png`,fullPage:true});
  result.media.push({name,url,before,after,additionalImageResponses:network});
  if(name==='pdp'){
   const selects=await p.$$('#single-product select[name^="variation"]');
   if(selects.length){const options=await selects[0].evaluate(e=>[...e.options].map(o=>({value:o.value,text:o.textContent,disabled:o.disabled,selected:o.selected})));const candidate=options.find(o=>!o.disabled&&!o.selected);
    const read=()=>p.evaluate(()=>({url:location.href,price:document.querySelector('#single-product .js-price-display')?.textContent,submit:document.querySelector('#single-product [type=submit]')?.textContent,variant:document.querySelector('#single-product input[name=variant]')?.value}));const before=await read();
    if(candidate){await selects[0].select(candidate.value);await p.waitForNetworkIdle({idleTime:300,timeout:5000}).catch(()=>{});result.states.push({name:'pdp-variant-selection',options,before,after:await read()});}else result.states.push({name:'pdp-variant-selection',options,unavailable:'No hay otra opción habilitada en el selector observado'});
   }
  }
 }
 await fs.writeFile(`${evidenceRoot}/measurements/browser/state-audit.json`,JSON.stringify(result,null,2));console.log(JSON.stringify({states:result.states.map(s=>({name:s.name,escapeDisplay:s.closedByEscape?.display,focusOnOpen:s.opened?.focusInside,axe:s.axe?.violations.map(v=>v.id),unavailable:s.unavailable})),overflow:result.overflow,media:result.media.map(s=>({name:s.name,additionalImages:s.additionalImageResponses.length,duplicates:s.after.duplicates,duplicateIds:s.after.duplicateIds.length}))}));
}finally{await fs.writeFile(`${evidenceRoot}/measurements/browser/state-audit.json`,JSON.stringify(result,null,2));await browser.close()}
