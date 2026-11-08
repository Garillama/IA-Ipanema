#!/usr/bin/env node
// Runner de lectura: reutiliza runtime, auth y extracción del discovery V1.
import fs from 'node:fs/promises';
import path from 'node:path';
import {puppeteer,authenticate,cliRequire,cleanUrl,loadDependency} from './browser_runtime.mjs';
import {collectRendered,collectSEOProjection} from './page_collectors.mjs';

const job=JSON.parse(await fs.readFile(process.argv[2],'utf8'));
const linkContracts=JSON.parse(await fs.readFile(new URL('./ipanema/seo/link_contracts.json',import.meta.url),'utf8'));
const out=path.resolve(job.output);
await fs.mkdir(out,{recursive:true});
const result={kind:'browser-qa',at:new Date().toISOString(),project:job.project,records:[],checks:[],limitations:[
 'Chrome automatizado; sin certificación WCAG ni lector de pantalla humano.',
 'Geometría: solapamientos y recortes son candidatos para revisión; no toda intersección es un defecto.',
 'HTML, DOM y enlaces no prueban indexación real. No se envían formularios comerciales.',
 'Métricas de laboratorio; sin INP de campo. Bytes recibidos no prueban decodificación o visibilidad de imágenes.',
 'La red de escritura está bloqueada: apps o lecturas por POST pueden comportarse distinto. No atribuir ese efecto al tema sin reproducción autorizada; comparar bajo la misma protección.'
]};
const check=(name,passed,details)=>result.checks.push({name,status:passed?'passed':'failed',details});
let browser;
try{
 browser=await puppeteer.launch();
 result.environment={browser:await browser.version(),node:process.versions.node,os:process.platform};
 const cookies=await authenticate(browser,job.pages[0].url);
 for(const spec of job.pages){
  const modes=job.mode==='full'?['rendered','no-js','reduced-motion']:['rendered'];
  for(const mode of modes)for(const width of (mode==='rendered'?job.widths:[job.widths[0]])){
   const context=await browser.createBrowserContext();if(cookies.length)await context.setCookie(...cookies);
   try{
    const page=await context.newPage();await page.setViewport({width,height:900,isMobile:width<768,hasTouch:width<768,deviceScaleFactor:1});
    if(mode==='no-js')await page.setJavaScriptEnabled(false);
    if(mode==='reduced-motion')await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
    const client=await page.createCDPSession();await client.send('Network.enable');await client.send('Network.setCacheDisabled',{cacheDisabled:true});
    if(job.cpu_rate)await client.send('Emulation.setCPUThrottlingRate',{rate:job.cpu_rate});
    if(job.network)await client.send('Network.emulateNetworkConditions',{offline:false,...job.network});
    const network=new Map();const errors=[];let phase='navigation';
    client.on('Network.requestWillBeSent',e=>network.set(e.requestId,{url:cleanUrl(e.request.url),method:e.request.method,type:e.type,requested:true,phase}));
    client.on('Network.responseReceived',e=>Object.assign(network.get(e.requestId)||{},{status:e.response.status,mime:e.response.mimeType}));
    client.on('Network.loadingFinished',e=>Object.assign(network.get(e.requestId)||{},{completed:true,encoded_bytes:e.encodedDataLength}));
    client.on('Network.loadingFailed',e=>Object.assign(network.get(e.requestId)||{},{completed:false,error:e.errorText}));
    page.on('pageerror',()=>errors.push('Error JavaScript en la página; inspeccionar localmente sin volcar datos.'));
    await page.evaluateOnNewDocument(()=>{
     window.__audit={lcp:[],shifts:[],longTasks:[]};
     for(const [type,key] of [['largest-contentful-paint','lcp'],['layout-shift','shifts'],['longtask','longTasks']])try{new PerformanceObserver(list=>window.__audit[key].push(...list.getEntries().map(e=>({startTime:e.startTime,duration:e.duration,value:e.value,hadRecentInput:e.hadRecentInput,size:e.size})))).observe({type,buffered:true});}catch{}
    });
    if(job.coverage&&mode!=='no-js'){await page.coverage.startJSCoverage();await page.coverage.startCSSCoverage();}
    const response=await page.goto(spec.url,{waitUntil:'domcontentloaded',timeout:30000});
    if(new URL(page.url()).pathname.startsWith('/password'))throw Error('La página final es una barrera de acceso, no el storefront.');
    const initialHTML=await response.text();
    const initial=await page.evaluate((html,contracts)=>{
     const d=new DOMParser().parseFromString(html,'text/html');
     return {title:d.title,h1:[...d.querySelectorAll('h1')].map(e=>({text:e.textContent.trim(),in_user_content:!!e.closest('.user-content')})),
      headings:[...d.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e=>({tag:e.tagName,text:e.textContent.trim()})),
      canonical:[...d.querySelectorAll('link[rel="canonical"]')].map(e=>e.getAttribute('href')),
      robots:[...d.querySelectorAll('meta[name=robots]')].map(e=>e.content),
      links:[...d.querySelectorAll('a')].map(e=>({href:e.getAttribute('href'),text:e.textContent.trim(),action_hint:new RegExp(contracts.native_action_pattern,'i').test(e.className)||e.getAttribute('role')==='button',carousel:!!e.closest('[data-qa-carousel],.swiper,.swiper-container,[data-component="slider"]')})),
      jsonld:[...d.querySelectorAll('script[type="application/ld+json"]')].map(e=>{try{JSON.parse(e.textContent);return {valid:true};}catch{return {valid:false};}}),
      breadcrumbs:[...d.querySelectorAll('[aria-label*="readcrumb"],.breadcrumb,[data-component="breadcrumbs"] a')].map(e=>({tag:e.tagName,href:e.getAttribute('href')})),
      product_count:d.querySelectorAll('[data-product-id]').length};
    },initialHTML,linkContracts);
    await page.waitForNetworkIdle({idleTime:400,timeout:5000}).catch(()=>{});
    await page.evaluate(()=>document.fonts.ready);
    const navigationNetwork=[...network.values()].map(entry=>({...entry}));
    const networkMetrics={requests:navigationNetwork.length};
    for(const [name,type] of [['js_bytes','Script'],['css_bytes','Stylesheet'],['image_bytes','Image'],['font_bytes','Font']])networkMetrics[name]=navigationNetwork.filter(e=>e.type===type&&e.completed).reduce((n,e)=>n+(e.encoded_bytes||0),0);
    for(const [name,value] of Object.entries(networkMetrics))if(job.budgets?.[name]!=null)check(`${spec.name}-${width}-${mode}:budget:${name}`,value<=job.budgets[name],{value,budget:job.budgets[name],method:'CDP solicitudes y encodedDataLength de navegación, antes de axe/interacciones'});
    phase='dom-inspection';
    // Capture before axe, masks, interactions and full-page screenshots alter DOM/network.
    let seoProjection=null;
    if(job.capture_seo){
     const allowedHeaders={};for(const key of ['x-robots-tag','content-type','content-language','location'])if(response.headers()[key])allowedHeaders[key]=response.headers()[key];
     seoProjection={kind:'seo-browser-projection',project:job.project,page:spec.name,page_type:spec.page_type||spec.name,
      url:cleanUrl(page.url()),at:new Date().toISOString(),status:response.status(),headers:allowedHeaders,
      width,mode,initial:await collectSEOProjection(page,initialHTML),rendered:await collectSEOProjection(page)};
    }
    const sample=await collectRendered(page);
    for(const image of sample.images)for(const k of ['src','currentSrc'])if(image[k])image[k]=cleanUrl(image[k]);
    sample.resources.forEach(r=>r.name=cleanUrl(r.name));
    sample.links.forEach(r=>r.href=cleanUrl(r.href));
    sample.metadata.forEach(r=>{if(r.href)r.href=cleanUrl(r.href);});
    const geometry=await page.evaluate(selector=>{
     const root=selector?document.querySelector(selector):document.body;
     if(!root)return {missing_component:true};
     const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'&&s.opacity!=='0';};
     const name=e=>({tag:e.tagName,id:e.id,class:typeof e.className==='string'?e.className:''});
     const elements=[root,...root.querySelectorAll('*')].filter(visible);
     const overflows=elements.filter(e=>{const r=e.getBoundingClientRect();if(r.left>=-1&&r.right<=innerWidth+1)return false;let p=e.parentElement;while(p&&p!==document.body){if(['hidden','clip','auto','scroll'].includes(getComputedStyle(p).overflowX))return false;p=p.parentElement;}return true;}).slice(0,30).map(name);
     const clipped=elements.filter(e=>['hidden','clip'].includes(getComputedStyle(e).overflowX)&&e.scrollWidth>e.clientWidth+1).slice(0,20).map(name);
     const controls=elements.filter(e=>e.matches('button,a,input,select,[role=button]')).slice(0,200);const overlaps=[];
     for(let i=0;i<controls.length;i++)for(let j=i+1;j<controls.length;j++){
      const a=controls[i],b=controls[j];if(a.contains(b)||b.contains(a))continue;
      const r=a.getBoundingClientRect(),s=b.getBoundingClientRect();const area=Math.max(0,Math.min(r.right,s.right)-Math.max(r.left,s.left))*Math.max(0,Math.min(r.bottom,s.bottom)-Math.max(r.top,s.top));
      if(area>0.25*Math.min(r.width*r.height,s.width*s.height)&&overlaps.length<20)overlaps.push([name(a),name(b)]);
     }
     const reading=elements.filter(e=>e.matches('[data-qa-order]')).map(e=>({key:e.dataset.qaOrder,top:e.getBoundingClientRect().top,left:e.getBoundingClientRect().left}));
     return {viewport:innerWidth,scroll_width:document.documentElement.scrollWidth,overflow_candidates:overflows,clipping_candidates:clipped,overlap_candidates:overlaps,reading_order:reading};
    },job.component_selector||null);
    const label=`${spec.name}-${width}-${mode}`;
    if(seoProjection)await fs.writeFile(path.join(out,label+'.seo.json'),JSON.stringify(seoProjection,null,2));
    check(label+':http',response.status()===(spec.expected_status||200),{actual:response.status(),expected:spec.expected_status||200});
    check(label+':overflow',!geometry.missing_component&&geometry.scroll_width<=width+1,geometry);
    if(mode==='rendered'){
     check(label+':h1',initial.h1.length===(spec.expected_h1??1),{count:initial.h1.length,locations:initial.h1});
     check(label+':title',!!initial.title.trim());
     check(label+':jsonld',initial.jsonld.every(j=>j.valid),initial.jsonld);
     if(spec.expect_canonical!==false)check(label+':canonical',initial.canonical.length===1,initial.canonical);
     check(label+':carousel-links',initial.links.filter(e=>e.carousel&&!e.action_hint).every(e=>!!e.href&&!/^(javascript:|#|$)/i.test(e.href)),initial.links.filter(e=>e.carousel&&!e.action_hint));
     for(const test of job.link_assertions||[]){const found=initial.links.some(e=>e.href&&new URL(e.href,spec.url).pathname===test.path);check(label+':link:'+test.path,found);}
    }
    if(mode==='no-js'){
     const invisible=sample.images.filter(i=>i.display!=='none'&&i.visible&&i.naturalWidth<2);
     const transparent=await page.evaluate(()=>[...document.images].filter(e=>e.getBoundingClientRect().top<innerHeight&&e.getBoundingClientRect().bottom>0&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).opacity==='0').length);
     check(label+':essential-images',invisible.length===0&&transparent===0,{unloaded:invisible.length,transparent});
    }
    let axe=null;
    if(mode==='rendered'&&job.axe!==false){
     phase='accessibility-instrumentation';
     await page.addScriptTag({path:cliRequire.resolve('axe-core')});
     axe=await page.evaluate(async selector=>{const r=await window.axe.run(selector?document.querySelector(selector):document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return {version:r.testEngine.version,violations:r.violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})),incomplete:r.incomplete.map(v=>v.id)};},job.component_selector||null);
     check(label+':axe',axe.violations.length===0,axe);
    }
    const interactionResults=[];
    phase='interaction';
    if(mode==='rendered')for(const interaction of job.interactions||[]){
     if(interaction.page&&interaction.page!==spec.name||interaction.widths&&!interaction.widths.includes(width))continue;
     for(const step of interaction.steps){
      const target=step.selector?await page.$(step.selector):null;
      if(step.action==='click'){
       if(!target)throw Error('Control de interacción no disponible.');
       const allowed=await target.evaluate(e=>{const form=e.closest('form');const anchor=e.closest('a[href]');return !(e.matches('[type=submit],input')||form&&e.tagName==='BUTTON'&&e.type!=='button'||/add.?to.?cart|checkout|comprar|buy.?now|js-prod-submit|js-addtocart/i.test(e.className+' '+e.id)||anchor&&/checkout|\/cart\/(add|update|remove)/i.test(anchor.getAttribute('href')));});
       if(!allowed)throw Error('Interacción rechazada: posible operación comercial.');await target.click();
      }else if(step.action==='press'){
       if(!['Escape','Tab','ArrowLeft','ArrowRight','ArrowDown','ArrowUp','Home','End'].includes(step.key))throw Error('Tecla de interacción no permitida.');await page.keyboard.press(step.key);
      }else if(step.action==='select'){
       if(!target)throw Error('Selector de variante ausente.');await page.select(step.selector,step.value);
      }else if(['assert_visible','assert_hidden','assert_focus'].includes(step.action)){
       if(step.action==='assert_visible')await page.waitForSelector(step.selector,{visible:true,timeout:3000}).catch(()=>{});
       if(step.action==='assert_hidden')await page.waitForSelector(step.selector,{hidden:true,timeout:3000}).catch(()=>{});
       const state=await page.evaluate((selector)=>{const e=document.querySelector(selector);const r=e?.getBoundingClientRect();return {visible:!!(e&&r.width&&r.height&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'),focus:!!e?.contains(document.activeElement)};},step.selector);
       const passed=step.action==='assert_visible'?state.visible:step.action==='assert_hidden'?!state.visible:state.focus;
       check(label+':'+interaction.name+':'+step.action,passed,state);interactionResults.push({name:interaction.name,step:step.action,passed});
      }else throw Error('Acción de interacción desconocida.');
     }
    }
    if(job.masks?.length){await page.addStyleTag({content:job.masks.map(selector=>`${selector}{visibility:hidden !important}`).join('\n')});}
    phase='screenshot';
    await page.screenshot({path:path.join(out,label+'.png'),fullPage:true});
    let coverage=null;
    if(job.coverage&&mode!=='no-js'){
     const js=await page.coverage.stopJSCoverage(),css=await page.coverage.stopCSSCoverage();
     const summarize=entries=>entries.map(e=>({url:cleanUrl(e.url),source_bytes:Buffer.byteLength(e.text),used_source_units:e.ranges.reduce((n,r)=>n+r.end-r.start,0),source_units:e.text.length}));
     coverage={js:summarize(js),css:summarize(css),limitations:'Coverage de esta navegación, no prueba código prescindible en otros estados; unidades UTF-16 y bytes distintos.'};
    }
    const record={page:spec.name,profile:{width,mode,cpu_rate:job.cpu_rate||1,network:job.network||null},at:new Date().toISOString(),status:response.status(),final_url:cleanUrl(page.url()),initial,sample,geometry,axe,interactions:interactionResults,network_metrics:networkMetrics,navigation_network:navigationNetwork,network:[...network.values()],errors,coverage};
    await fs.writeFile(path.join(out,label+'.json'),JSON.stringify(record,null,2));
    result.records.push({page:spec.name,width,mode,file:label+'.json',screenshot:label+'.png'});
   }finally{await context.close();}
  }
 }
 if(job.lighthouse){
  const lighthouse=(await loadDependency('lighthouse')).default;
  const desktop=(await loadDependency('lighthouse/core/config/desktop-config.js')).default;
  const port=Number(new URL(browser.wsEndpoint()).port);
  if(cookies.length)await browser.defaultBrowserContext().setCookie(...cookies);
  for(const spec of job.pages)for(const profile of ['mobile','desktop']){
   const {lhr}=await lighthouse(spec.url,{port,output:'json',logLevel:'error',disableStorageReset:true,onlyCategories:['performance'],blockedUrlPatterns:['*checkout*','*/cart/add*','*/cart/update*','*/cart/remove*']},profile==='desktop'?desktop:undefined);
   if(browser.__accessLimited)throw Error('HTTP '+browser.__accessLimited+': detenido sin reintentos.');
   if(browser.__protectionError)throw Error('No se pudo proteger una pestaña; auditoría detenida.');
   if(lhr.runtimeError||new URL(lhr.finalDisplayedUrl).pathname.startsWith('/password'))throw Error('Lighthouse no midió la página requerida.');
   const metrics={lcp_ms:lhr.audits['largest-contentful-paint'].numericValue,cls:lhr.audits['cumulative-layout-shift'].numericValue,tbt_ms:lhr.audits['total-blocking-time'].numericValue};
   const artifact={page:spec.name,profile,at:lhr.fetchTime,lighthouse_version:lhr.lighthouseVersion,config:lhr.configSettings,network_policy:'read-only-all-tabs-v1',environment:result.environment,metrics,field_inp:null,warnings:lhr.runWarnings};
   await fs.writeFile(path.join(out,`${spec.name}-${profile}-metrics.json`),JSON.stringify(artifact,null,2));
   for(const [name,value] of Object.entries(metrics))if(job.budgets?.[name]!=null)check(`${spec.name}:${profile}:${name}`,value<=job.budgets[name],{value,budget:job.budgets[name],type:'proposed_budget'});
  }
 }
}catch(error){result.error=String(error.message);result.outcome=/HTTP (403|429)|Acceso limitado|barrera de acceso/.test(result.error)?'blocked':'failed';}
finally{if(browser)await browser.close();result.outcome??=result.checks.some(c=>c.status==='failed')?'failed':'passed';await fs.writeFile(path.join(out,'browser-report.json'),JSON.stringify(result,null,2));}
console.log(JSON.stringify({outcome:result.outcome,checks:result.checks.length,failed:result.checks.filter(c=>c.status==='failed').length,error:result.error}));
process.exitCode=result.outcome==='passed'?0:result.outcome==='blocked'?2:1;
