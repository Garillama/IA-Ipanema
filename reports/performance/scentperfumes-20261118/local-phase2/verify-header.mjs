// Controlled component replay, not Twig/storefront or CWV evidence. Loopback only.
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {puppeteer} from '../../../../tools/browser_runtime.mjs';
const out=path.dirname(fileURLToPath(import.meta.url));
const theme='/home/alanrichard/Codefy/scentperfumesclaude';
const draft='/home/alanrichard/Escritorio/IA inversa/.local/scent-phase2-20261118';
const sources={before:await fs.readFile(theme+'/static/js/sc-scent-extras.js','utf8'),after:await fs.readFile(draft+'/static/js/sc-scent-extras.js','utf8')};
const html=version=>`<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Header measurement fixture</title><style>
body{margin:0;font:16px system-ui;background:white;color:black;min-height:3000px}.draft-bar{position:fixed;inset:0 0 auto;height:32px;background:#222;color:white;z-index:100}.draft-bar.is-collapsed{height:0;overflow:hidden}.sticky-header-wrapper.is-fixed{position:fixed;inset:0 0 auto}.header{position:relative;top:var(--scent-draft-h,0px);height:80px;background:#eee;box-sizing:border-box}header a{display:inline-block;padding:20px;color:#111}main{padding-top:160px}nav{position:fixed;top:var(--scent-pills-top,80px);background:#eee}@media(max-width:500px){.header{height:64px}}
</style><div class="draft-bar">Borrador</div><div class="sticky-header-wrapper is-fixed"><header class="js-head-main js-header header"><a href="#main">Scent</a></header></div><nav>Perfumes</nav><main id="main"><h1>Prueba local de cabecera</h1></main><script src="/${version}.js"></script></html>`;
const requests=[];
const server=http.createServer((req,res)=>{requests.push(req.url);const m=req.url.match(/^\/(before|after)(\.js)?$/);if(!m){res.writeHead(404);res.end();return;}res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',m[2]?'text/javascript':'text/html');res.end(m[2]?sources[m[1]]:html(m[1]));});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
process.env.IPANEMA_RESOURCE_ORIGINS=origin;
const result={at:new Date().toISOString(),scope:'local synthetic header DOM with full original/candidate extras script; no storefront measurements',profiles:{390:{height:844,cpu:4},1440:{height:844,cpu:1}},samples:[],checks:[],remote_requests:0};let browser;
const delay=ms=>new Promise(r=>setTimeout(r,ms));
try{
 browser=await puppeteer.launch();result.browser=await browser.version();
 for(const width of [390,1440])for(let run=0;run<3;run++)for(const version of (run%2?['after','before']:['before','after'])){
  const context=await browser.createBrowserContext(),page=await context.newPage();
  await page.setViewport({width,height:844,isMobile:width===390,hasTouch:width===390,deviceScaleFactor:1});
  const client=await page.createCDPSession();await client.send('Network.enable');await client.send('Network.setCacheDisabled',{cacheDisabled:true});await client.send('Performance.enable');await client.send('Emulation.setCPUThrottlingRate',{rate:width===390?4:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.evaluateOnNewDocument(()=>{window.writes=0;window.longTasks=[];const set=CSSStyleDeclaration.prototype.setProperty;CSSStyleDeclaration.prototype.setProperty=function(k,v,...args){if(k.startsWith('--scent-'))window.writes++;return set.call(this,k,v,...args);};new PerformanceObserver(list=>{for(const e of list.getEntries())window.longTasks.push(e.duration);}).observe({type:'longtask',buffered:true});});
  await page.goto(origin+'/'+version,{waitUntil:'load'});await delay(2200);
  const check=(name,passed)=>result.checks.push({width,run,version,name,passed});
  const state=()=>page.evaluate(()=>{const s=document.documentElement.style;return ['--scent-draft-h','--scent-hdr-h','--scent-pills-top'].map(k=>s.getPropertyValue(k));});
  check('initial-draft-offset',JSON.stringify(await state())===JSON.stringify(['32px',width===390?'64px':'80px',width===390?'96px':'112px']));
  const start=Object.fromEntries((await client.send('Performance.getMetrics')).metrics.map(m=>[m.name,m.value]));
  const writes=await page.evaluate(async()=>{const before=window.writes;for(let i=0;i<30;i++){window.dispatchEvent(new Event('scroll'));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));}return window.writes-before;});
  const end=Object.fromEntries((await client.send('Performance.getMetrics')).metrics.map(m=>[m.name,m.value]));
  check('stable-scroll-write-count',writes===(version==='before'?90:0));
  // Actual scroll plus draft toolbar and responsive geometry changes.
  await page.evaluate(()=>{window.scrollTo(0,600);document.querySelector('.draft-bar').classList.add('is-collapsed');});await delay(420);
  check('collapsed-draft',JSON.stringify(await state())===JSON.stringify(['0px',width===390?'64px':'80px',width===390?'64px':'80px']));
  await page.evaluate(()=>document.querySelector('header').style.height='100px');await delay(80);
  check('resize-observer-keeps-offsets',JSON.stringify(await state())===JSON.stringify(['0px','100px','100px']));
  await page.evaluate(()=>document.querySelector('.draft-bar').classList.remove('is-collapsed'));await delay(420);
  check('expanded-draft',JSON.stringify(await state())===JSON.stringify(['32px','100px','132px']));
  await page.evaluate(()=>{document.documentElement.style.setProperty('--scent-draft-h','99px');window.dispatchEvent(new Event('scroll'));});await delay(70);
  check('repairs-external-inline-write',(await state())[0]==='32px');
  await page.focus('header a');check('keyboard-focus-preserved',await page.$eval('header a',n=>n===document.activeElement));
  await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
  check('no-script-errors',errors.length===0);
  const screenshot=`header-${width}-${run}-${version}.png`;await page.screenshot({path:path.join(out,screenshot)});
  const metrics={};for(const k of ['TaskDuration','ScriptDuration','LayoutDuration','RecalcStyleDuration','LayoutCount','RecalcStyleCount'])metrics[k]=end[k]-start[k];
  result.samples.push({width,run,version,writes,metrics,long_tasks:await page.evaluate(()=>window.longTasks),errors,screenshot,final_state:await state()});await context.close();
 }
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
result.passed=result.checks.every(c=>c.passed);result.request_count=requests.length;
await fs.writeFile(path.join(out,'header-browser.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({passed:result.passed,checks:result.checks.length,samples:result.samples.length,failures:result.checks.filter(c=>!c.passed)}));if(!result.passed)process.exitCode=1;
