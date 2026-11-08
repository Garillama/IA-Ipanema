#!/usr/bin/env node
// Navegación GET: no carrito escrito, cuentas creadas, newsletter ni configuración.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {puppeteer,authenticate,cliRequire,evidenceRoot} from './browser_runtime.mjs';
const start=process.argv[2];if(!start)throw Error('URL inicial necesaria.');
const origin=new URL(start).origin;
const out=path.resolve(`${evidenceRoot}/measurements/crawl`);
const shots=path.resolve(`${evidenceRoot}/screenshots/routes`);
await fs.mkdir(out,{recursive:true});await fs.mkdir(shots,{recursive:true});
const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
const queue=[],seen=new Set(),results=[],skipped=[];
function enqueue(raw,from){
 let u;try{u=new URL(raw,origin);}catch{return;}
 if(u.origin!==origin||!['http:','https:'].includes(u.protocol))return;
 if(/\/admin(?:\/|$)|\/logout|\/sair|\/cdn-cgi\/|\/cart\/(?:add|remove|update)|\/winnie-pooh|\.(?:png|jpe?g|webp|avif|svg|gif|pdf|xml|txt|js|css)$/i.test(u.pathname)){skipped.push({url:u.href,reason:'Fuera de rutas de contenido o acción excluida',from});return;}
 u.hash='';
 for(const key of [...u.searchParams.keys()])if(!['page','q'].includes(key))u.searchParams.delete(key);
 const key=u.href;
 if(seen.has(key)||queue.some(x=>x.url===key))return;
 queue.push({url:key,from});
}
try{
 const cookies=await authenticate(browser,start);
 const context=await browser.createBrowserContext();if(cookies.length)await context.setCookie(...cookies);
 const page=await context.newPage();await page.setViewport({width:1440,height:1000});await page.goto(start,{waitUntil:'domcontentloaded',timeout:45000});
 const resources=await page.evaluate(async()=>{const all=[];for(const name of ['robots.txt','sitemap.xml']){try{const r=await fetch('/'+name);all.push({name,url:r.url,status:r.status,contentType:r.headers.get('content-type'),text:await r.text()});}catch(e){all.push({name,error:String(e)})}}return all;});
 for(const r of resources){
  // Guardar solo texto público de rastreo, nunca HTML de acceso con campos temporales.
  if(r.text&&!r.text.trimStart().startsWith('<!DOCTYPE html>')&&!r.url?.includes('/password')){
   await fs.writeFile(path.join(out,r.name),r.text);
   if(r.name==='sitemap.xml')for(const match of r.text.matchAll(/<loc>\s*([^<]+)\s*<\/loc>/g)){
    if(match[1].endsWith('.xml'))continue;enqueue(match[1],'sitemap.xml');
   }
  }
 }
 await fs.writeFile(path.join(out,'crawl-endpoints.json'),JSON.stringify(resources.map(({text,...r})=>({...r,bytes:text?.length,sha256:text?crypto.createHash('sha256').update(text).digest('hex'):null,htmlInsteadOfEndpoint:!!text?.trimStart().startsWith('<!DOCTYPE html>')})),null,2));
 enqueue(origin+'/','inicio');enqueue(origin+'/search/?q=rhino','formulario GET observado: search q');enqueue(origin+'/search/?q=__ipanema_audit_no_result_20261108__','estado sin resultados');enqueue(origin+'/comprar/','store.cart_url observado en formularios');enqueue(origin+'/__ipanema_discovery_404__/','sonda sintética 404');
 while(queue.length&&results.length<150){
  const item=queue.shift();if(seen.has(item.url))continue;seen.add(item.url);
  const slug=crypto.createHash('sha256').update(item.url).digest('hex').slice(0,12);
  const network=[],errors=[];const handler=res=>{if(res.request().resourceType()==='document')network.push({url:res.url(),status:res.status()});};const onError=e=>errors.push(String(e));page.on('response',handler);page.on('pageerror',onError);
  try{
   const response=await page.goto(item.url,{waitUntil:'domcontentloaded',timeout:40000});
   if([403,429].includes(response.status())){
    const rec={...item,slug,status:response.status(),error:'Acceso limitado; crawl detenido sin reintentos'};results.push(rec);await fs.writeFile(path.join(out,slug+'.json'),JSON.stringify(rec,null,2));break;
   }
   const initialHtml=await response.text();
   const initial=await page.evaluate(html=>{const d=new DOMParser().parseFromString(html,'text/html');return {title:d.title,h1:[...d.querySelectorAll('h1')].map(x=>x.textContent.trim()),links:[...d.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')),images:[...d.images].map(x=>({src:x.getAttribute('src'),srcset:x.getAttribute('srcset'),dataSrc:x.getAttribute('data-src'),dataSrcset:x.getAttribute('data-srcset'),loading:x.getAttribute('loading'),fetchpriority:x.getAttribute('fetchpriority'),width:x.getAttribute('width'),height:x.getAttribute('height')})),jsonld:[...d.querySelectorAll('script[type="application/ld+json"]')].map(x=>{try{const v=JSON.parse(x.textContent);return {component:x.dataset.component,type:v['@type'],mainEntityType:v.mainEntity?.['@type']}}catch(e){return {component:x.dataset.component,error:String(e)}}})};},initialHtml);
   await page.waitForNetworkIdle({idleTime:500,timeout:7000}).catch(()=>{});
   const dom=await page.evaluate(()=>({url:location.href,title:document.title,lang:document.documentElement.lang,bodyClass:document.body.className,h1:[...document.querySelectorAll('h1')].map(x=>x.textContent.trim()),headings:[...document.querySelectorAll('h2,h3')].map(x=>({tag:x.tagName,text:x.textContent.trim()})),canonical:[...document.querySelectorAll('link[rel="canonical"]')].map(x=>x.href),robots:[...document.querySelectorAll('meta[name="robots"]')].map(x=>x.content),description:document.querySelector('meta[name="description"]')?.content,hreflang:[...document.querySelectorAll('link[hreflang]')].map(x=>({lang:x.hreflang,href:x.href})),links:[...document.querySelectorAll('a[href]')].map(x=>({url:x.href,text:x.textContent.trim(),rel:x.rel})),forms:[...document.forms].map(x=>({action:x.action,method:x.method,fieldNames:[...x.elements].map(e=>e.name).filter(Boolean)})),sections:[...document.querySelectorAll('[data-section-type]')].map(x=>({id:x.id,type:x.dataset.sectionType})),images:[...document.images].map(x=>({src:x.currentSrc,alt:x.getAttribute('alt'),width:x.width,height:x.height,naturalWidth:x.naturalWidth,loading:x.loading,fetchPriority:x.fetchPriority})),productContainers:[...document.querySelectorAll('[data-variants]')].slice(0,2).map(x=>{try{return {id:x.id,variants:JSON.parse(x.getAttribute('data-variants')),contactUrl:x.getAttribute('data-contact-url')}}catch{return {id:x.id,error:'no parseable'}}}),contactUrls:[...document.querySelectorAll('[data-contact-url]')].map(x=>x.getAttribute('data-contact-url')),domNodes:document.getElementsByTagName('*').length,scrollWidth:document.documentElement.scrollWidth,innerWidth:innerWidth,text:document.querySelector('main')?.innerText.slice(0,3000)}));
   for(const link of dom.links)enqueue(link.url,item.url);for(const u of dom.contactUrls)enqueue(u,item.url+' data-contact-url');
   const counts=Object.fromEntries(['Product','Offer','BreadcrumbList','Organization'].map(type=>[type,(initialHtml.match(new RegExp('"@type"\\s*:\\s*"'+type+'"','g'))||[]).length]));
   let axe=null;
   if(/template-(?:home|category|product|search|cart|contact|404|blog|page)\b/.test(dom.bodyClass)&&(!results.some(x=>x.dom?.bodyClass===dom.bodyClass)||item.url.includes('__ipanema'))){
    await page.addScriptTag({path:cliRequire.resolve('axe-core')});axe=await page.evaluate(async()=>{const r=await window.axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return {engine:r.testEngine,violations:r.violations,incomplete:r.incomplete,passes:r.passes.map(x=>x.id)};});
   }
   await page.screenshot({path:path.join(shots,slug+'-1440.png'),fullPage:true});
   await page.setViewport({width:390,height:900,isMobile:true,hasTouch:true});
   await page.screenshot({path:path.join(shots,slug+'-390.png'),fullPage:true});
   const mobile=await page.evaluate(()=>({innerWidth,scrollWidth:document.documentElement.scrollWidth,horizontalOverflow:document.documentElement.scrollWidth>innerWidth,headings:[...document.querySelectorAll('h1')].map(x=>x.innerText)}));
   await page.setViewport({width:1440,height:1000,isMobile:false,hasTouch:false});
   const record={...item,slug,verifiedAt:new Date().toISOString(),status:response.status(),finalUrl:page.url(),navigationChain:network,initial,structuredDataCounts:counts,dom,mobile,axe,errors,xRobotsTag:response.headers()['x-robots-tag']||null};results.push(record);
   await fs.writeFile(path.join(out,slug+'.json'),JSON.stringify(record,null,2));
   console.log(JSON.stringify({n:results.length,url:item.url,final:record.finalUrl,status:record.status,template:dom.bodyClass,h1:dom.h1.length,axe:axe?.violations.map(v=>v.id),queued:queue.length}));
  }catch(e){const rec={...item,slug,error:String(e)};results.push(rec);await fs.writeFile(path.join(out,slug+'.json'),JSON.stringify(rec,null,2));console.log(JSON.stringify(rec));}
  finally{page.off('response',handler);page.off('pageerror',onError);}
 }
 await fs.writeFile(path.join(out,'summary.json'),JSON.stringify({verifiedAt:new Date().toISOString(),method:'Crawl GET con sesión storefront autorizada, sin formularios comerciales',pages:results.map(({url,slug,status,finalUrl,error,dom,mobile,axe})=>({url,slug,status,finalUrl,error,bodyClass:dom?.bodyClass,h1:dom?.h1,overflowMobile:mobile?.horizontalOverflow,axeRules:axe?.violations.map(v=>v.id)})),remainingQueue:queue,skipped,limitations:['Máximo 150 rutas para evitar espacios infinitos; ver cola restante.','Normaliza queries a page/q; no explora todas las combinaciones de filtros y variantes.','Screenshots mobile tras resize; no es recarga fría móvil ni prueba independiente de touch.','No crea carrito, clientes, compras, suscripciones ni envía newsletter/contacto.','No conserva contraseña ni cookies.']},null,2));
}finally{await browser.close();}
