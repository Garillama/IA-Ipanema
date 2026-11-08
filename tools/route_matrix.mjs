#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {puppeteer,authenticate,cliRequire} from './browser_runtime.mjs';
const summary=JSON.parse(await fs.readFile('ipanema-discovery/13-evidence/measurements/crawl/summary.json','utf8'));
const representative=new Map();
for(const r of summary.pages)if(r.bodyClass?.trim()&&!r.error&&!representative.has(r.bodyClass.trim()))representative.set(r.bodyClass.trim(),r.url);
representative.delete('template-home'); // Ya tiene seis cargas independientes, no repetirlas.
const jobs=[];for(const [template,url] of representative)for(const width of [360,390,768,1024,1440,1920])jobs.push({template,url,width});
const out='ipanema-discovery/13-evidence/measurements/responsive-matrix';const shots='ipanema-discovery/13-evidence/screenshots/matrix';await fs.mkdir(out,{recursive:true});await fs.mkdir(shots,{recursive:true});
const browser=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--disable-dev-shm-usage']});const results=[];
try{
 const cookies=await authenticate(browser,'https://rhinoipanema.mitiendanube.com/?exit_preview_theme_installation');
 async function worker(){while(jobs.length){const job=jobs.shift();const ctx=await browser.createBrowserContext();await ctx.setCookie(...cookies);try{
  const page=await ctx.newPage();await page.setViewport({width:job.width,height:900,deviceScaleFactor:1,isMobile:job.width<768,hasTouch:job.width<768});
  const res=await page.goto(job.url,{waitUntil:'domcontentloaded',timeout:40000});await page.waitForNetworkIdle({idleTime:600,timeout:6000}).catch(()=>{});
  const dom=await page.evaluate(()=>({finalUrl:location.href,title:document.title,bodyClass:document.body.className,innerWidth,scrollWidth:document.documentElement.scrollWidth,h1:[...document.querySelectorAll('h1')].map(e=>e.textContent.trim()),images:document.images.length,domNodes:document.getElementsByTagName('*').length,sections:[...document.querySelectorAll('[data-section-type]')].map(e=>e.dataset.sectionType)}));
  let axe=null;if([390,1440].includes(job.width)){await page.addScriptTag({path:cliRequire.resolve('axe-core')});axe=await page.evaluate(async()=>{const r=await window.axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return {engine:r.testEngine,violations:r.violations,incomplete:r.incomplete,passes:r.passes.map(x=>x.id)};});}
  const record={...job,verifiedAt:new Date().toISOString(),status:res.status(),dom,axe,limitations:['Una ruta representativa de este template; no todas sus variantes.','Geometría y screenshot con recarga y emulación de dispositivo; no benchmark de velocidad.','Dos páginas concurrentes; no usar estos tiempos como medición de rendimiento.']};
  const name=job.template+'-'+job.width;await page.screenshot({path:path.join(shots,name+'.png'),fullPage:true});await fs.writeFile(path.join(out,name+'.json'),JSON.stringify(record,null,2));
  results.push({template:job.template,url:job.url,width:job.width,status:record.status,overflow:dom.scrollWidth>dom.innerWidth,axeRules:axe?.violations.map(x=>x.id)});
  console.log(JSON.stringify(results.at(-1)));
 }catch(e){const r={...job,error:String(e)};results.push(r);console.log(JSON.stringify(r));}finally{await ctx.close();}}}
 await Promise.all([worker(),worker()]);
}finally{await browser.close();await fs.writeFile(path.join(out,'summary.json'),JSON.stringify({verifiedAt:new Date().toISOString(),results},null,2));}
