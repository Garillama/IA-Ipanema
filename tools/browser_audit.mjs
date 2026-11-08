#!/usr/bin/env node
// Usa dependencias YA instaladas; no instala paquetes ni envía formularios.
import fs from 'node:fs/promises';
import path from 'node:path';
import {collectRendered} from './page_collectors.mjs';
import {cliRequire as require, puppeteer, authenticate,evidenceRoot} from './browser_runtime.mjs';
const url = process.argv[2];
const prefix=process.argv[3]||'';
if(!/^[a-z0-9-]*$/.test(prefix))throw Error('Prefijo no válido.');
if (!url || new URL(url).protocol !== 'https:') throw new Error('Indicar una URL HTTPS autorizada.');
const dest = path.resolve(`${evidenceRoot}`);
await fs.mkdir(path.join(dest, 'screenshots'), {recursive: true});
await fs.mkdir(path.join(dest, 'measurements/browser'), {recursive: true});
const cleanUrl = value => {
  try { const u = new URL(value); for (const key of [...u.searchParams.keys()]) if (/token|key|secret|auth|session|email|phone/i.test(key) && key !== 'theme_installation_id') u.searchParams.set(key, '[redacted]'); return u.href; }
  catch { return value; }
};
const browser = await puppeteer.launch({headless: true, args: ['--disable-dev-shm-usage']});
let accessCookies=[];
const configs = [360,390,768,1024,1440,1920].map(width=>({name: `viewport-${width}`, width, js:true}));
configs.push({name:'no-javascript-390',width:390,js:false}, {name:'reduced-motion-390',width:390,js:true,reduced:true}, {name:'slow-network-cpu4-390',width:390,js:true,slow:true});
const results = [];
try {
  accessCookies=await authenticate(browser,url);
  for (const config of configs) {
    const context = await browser.createBrowserContext();
    if(accessCookies.length)await context.setCookie(...accessCookies);
    const page = await context.newPage();
    await page.setViewport({width:config.width,height:900,deviceScaleFactor:1,isMobile:config.width<768,hasTouch:config.width<768});
    await page.setJavaScriptEnabled(config.js);
    if (config.reduced) await page.emulateMediaFeatures([{name:'prefers-reduced-motion', value:'reduce'}]);
    const client = await page.createCDPSession();
    await client.send('Network.enable');
    await client.send('Network.setCacheDisabled',{cacheDisabled:true});
    if (config.slow) {
      await client.send('Emulation.setCPUThrottlingRate',{rate:4});
      await client.send('Network.emulateNetworkConditions',{offline:false,latency:150,downloadThroughput:200000,uploadThroughput:93750});
    }
    const network = new Map(), failures=[], errors=[];
    client.on('Network.responseReceived',ev=>network.set(ev.requestId,{url:cleanUrl(ev.response.url),status:ev.response.status,mimeType:ev.response.mimeType,type:ev.type,fromDiskCache:ev.response.fromDiskCache,protocol:ev.response.protocol}));
    client.on('Network.loadingFinished',ev=>{const rec=network.get(ev.requestId);if(rec)rec.encodedDataLength=ev.encodedDataLength;});
    client.on('Network.loadingFailed',ev=>failures.push({type:ev.type,error:ev.errorText,canceled:ev.canceled}));
    page.on('pageerror',e=>errors.push(String(e)));
    await page.evaluateOnNewDocument(()=>{
      window.__audit={lcp:[],shifts:[],longTasks:[]};
      for(const [type,key] of [['largest-contentful-paint','lcp'],['layout-shift','shifts'],['longtask','longTasks']]) {
        try {new PerformanceObserver(list=>window.__audit[key].push(...list.getEntries().map(e=>({startTime:e.startTime,duration:e.duration,value:e.value,hadRecentInput:e.hadRecentInput,size:e.size,tag:e.element?.tagName,id:e.element?.id})))).observe({type,buffered:true});}catch{}
      }
    });
    const response = await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
    const finalUrl=page.url();
    await page.screenshot({path:path.join(dest,'screenshots',`${prefix}${config.name}-initial.png`)});
    await page.waitForNetworkIdle({idleTime:1000,timeout:12000}).catch(()=>{});
    const sample = await collectRendered(page);
    sample.resources.forEach(r=>r.name=cleanUrl(r.name));
    sample.images.forEach(r=>{for(const k of ['src','currentSrc'])if(r[k])r[k]=cleanUrl(r[k]);});
    await page.screenshot({path:path.join(dest,'screenshots',`${prefix}${config.name}-loaded.png`),fullPage:true});
    let axe=null;
    if(config.js && ['viewport-390','viewport-1440'].includes(config.name)) {
      await page.addScriptTag({path:require.resolve('axe-core')});
      axe=await page.evaluate(async()=>{
        const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});
        return {testEngine:r.testEngine,url:r.url,violations:r.violations,incomplete:r.incomplete,passes:r.passes.map(x=>({id:x.id,help:x.help})),inapplicable:r.inapplicable.map(x=>x.id)};
      });
    }
    const record={verifiedAt:new Date().toISOString(),requestedUrl:url,finalUrl,access:accessCookies.length?'Acceso storefront autorizado; sesión solo en memoria':'Sin sesión',config,status:response?.status(),browser:await browser.version(),responseHeaders:Object.fromEntries(Object.entries(response?.headers()||{}).filter(([k])=>['content-type','x-robots-tag','cache-control','content-encoding'].includes(k))),sample,network:[...network.values()],failures,errors,axe,limitations:['Muestra de laboratorio aislada; no es dato de campo ni INP.','La URL final puede ser una barrera de contraseña, no la página solicitada.','Solo se envió el formulario de acceso cuando se proporcionó autorización; no se enviaron formularios comerciales.','Las capturas initial y loaded no constituyen un filmstrip completo.']};
    await fs.writeFile(path.join(dest,'measurements/browser',`${prefix}${config.name}.json`),JSON.stringify(record,null,2));
    results.push({name:config.name,finalUrl,status:record.status,width:config.width,nodes:sample.domNodes,images:sample.images.length,requests:record.network.length,axeViolations:axe?.violations.length??null,overflow:sample.viewport.scrollWidth>sample.viewport.innerWidth});
    console.log(JSON.stringify(results.at(-1)));
    await context.close();
  }
} finally { await browser.close(); }
await fs.writeFile(path.join(dest,`measurements/browser/${prefix}summary.json`),JSON.stringify(results,null,2));
