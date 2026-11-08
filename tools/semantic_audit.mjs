#!/usr/bin/env node
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {puppeteer,authenticate,evidenceRoot,projectUrl,knowledgeFile} from './browser_runtime.mjs';
const crawl=JSON.parse(await fs.readFile(knowledgeFile('13-evidence/measurements/crawl/summary.json'),'utf8'));
const urls=[...new Set(crawl.pages.filter(x=>x.bodyClass?.trim()).map(x=>x.finalUrl))];
const b=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
try{
 const cookies=await authenticate(b,projectUrl());const ctx=await b.createBrowserContext();await ctx.setCookie(...cookies);const p=await ctx.newPage();await p.goto(projectUrl(),{waitUntil:'domcontentloaded'});
 const records=await p.evaluate(async urls=>{
  const pending=[...urls],records=[];let blocked=false;
  async function read(){while(pending.length&&!blocked){const url=pending.shift();try{const r=await fetch(url);if([403,429].includes(r.status)){blocked=true;records.push({url,status:r.status,error:'Acceso limitado; lectura detenida, sin reintentos'});break;}const html=await r.text();const d=new DOMParser().parseFromString(html,'text/html');const main=d.querySelector('main');
   const content=[...main?.querySelectorAll('.user-content')||[]].map(e=>e.textContent.replace(/\s+/g,' ').trim()).join('\n');
   const ids=[...d.querySelectorAll('[id]')].reduce((o,e)=>(o[e.id]=(o[e.id]||0)+1,o),{});
   records.push({url,status:r.status,finalUrl:r.url,title:d.title,lang:d.documentElement.lang,headings:[...d.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e=>({level:e.tagName,text:e.textContent.trim(),inUserContent:!!e.closest('.user-content')})),landmarks:Object.fromEntries(['main','header','footer','nav','section','article','aside'].map(tag=>[tag,d.querySelectorAll(tag).length])),initialDuplicateIds:Object.entries(ids).filter(([,n])=>n>1),imagesWithoutAlt:[...d.images].filter(e=>!e.hasAttribute('alt')).map(e=>({src:e.getAttribute('src'),class:e.className})),initialLinkCount:d.querySelectorAll('a[href]').length,anchorsWithoutHref:d.querySelectorAll('a:not([href])').length,userContentCharacters:content.length,contentForHash:content});
  }catch(e){records.push({url,error:String(e)})}}}
  await read();for(const url of pending)records.push({url,error:'No ejecutado después de límite de acceso'});return records;
 },urls);
 for(const record of records){if(record.contentForHash){record.userContentSha256=crypto.createHash('sha256').update(record.contentForHash).digest('hex');}delete record.contentForHash;}
 const duplicates=Object.entries(records.reduce((o,r)=>{if(r.userContentSha256)(o[r.userContentSha256]??=[]).push(r.url);return o;},{})).filter(([,v])=>v.length>1).map(([hash,urls])=>({hash,urls}));
 const checkout=records.some(r=>[403,429].includes(r.status))?{status:'no ejecutado por límite previo'}:await p.evaluate(async()=>{const r=await fetch('/checkout/');const d=new DOMParser().parseFromString(await r.text(),'text/html');const u=new URL(r.url);return {method:'GET a ruta observada en robots; sin envío de formulario',status:r.status,finalOrigin:u.origin,finalPath:u.pathname,title:d.title,bodyClass:d.body?.className};});
 const result={verifiedAt:new Date().toISOString(),method:'GET con sesión autorizada y DOMParser: HTML inicial, scripts de la respuesta no ejecutados',records,duplicateUserContent:duplicates,checkoutProbe:checkout,limitations:['No sustituye DOM interactivo, ARIA computada ni prueba de lector de pantalla.','Hash igual identifica texto user-content normalizado igual; no decide intención editorial ni canonical.','GET checkout vacío no prueba checkout con productos ni pagos.']};await fs.writeFile(`${evidenceRoot}/measurements/browser/semantic-audit.json`,JSON.stringify(result,null,2));
 console.log(JSON.stringify({routes:records.length,errors:records.filter(r=>r.error),duplicateUserContent:duplicates,checkout}));
}finally{await b.close()}
