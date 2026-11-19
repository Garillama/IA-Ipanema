// Executes the exact isolated media functions; never executes builder commerce code.
import fs from 'node:fs/promises';import http from 'node:http';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {puppeteer} from '../../../../tools/browser_runtime.mjs';
const out=path.dirname(fileURLToPath(import.meta.url)),theme='/home/alanrichard/Codefy/scentperfumesclaude',draft='/home/alanrichard/Escritorio/IA inversa/.local/scent-phase2-20261118';
const beforeOnly=process.argv.includes('--before-only'),extraOnly=process.argv.includes('--extra-only'),versions=beforeOnly?['before']:['before','after'];
const scripts={};for(const v of versions){const source=await fs.readFile((v==='before'?theme:draft)+'/static/js/sc-armador3.js','utf8');const start=source.indexOf('  function stopOthers(card)'),end=source.indexOf('  /* ---------- animaciones',start);if(start<0||end<0)throw Error('Media extraction contract changed');scripts[v]=source.slice(start,end);}
const media={};for(const n of ['sc-set-guey.mp4','sc-set-hector.mp4'])media[n]=await fs.readFile(theme+'/static/videos/'+n);
const html=v=>`<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Builder media replay</title><style>body{margin:0;font:16px system-ui}.spacer{height:1000px}.scc-vid{height:700px}video{display:block;width:240px;height:200px}button{height:44px}</style><div class="spacer">Contenido anterior</div><section id="root"><div class="scc-vid"><video preload="metadata" playsinline muted src="/sc-set-guey.mp4"></video><button>Reproducir primero</button></div><div class="scc-vid"><video preload="none" playsinline src="/sc-set-hector.mp4"></video><button>Reproducir segundo</button></div></section><div class="spacer"></div><script>var root=document.getElementById('root');${scripts[v]}root.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>playVideo(b.closest('.scc-vid'))));autoVideo();</script></html>`;
const requests=[];const server=http.createServer((req,res)=>{requests.push({url:req.url,method:req.method});const name=req.url.slice(1);if(media[name]){res.setHeader('Content-Type','video/mp4');res.end(media[name]);return;}if(versions.includes(name)){res.setHeader('Content-Type','text/html');res.end(html(name));return;}res.writeHead(404);res.end();});await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;process.env.IPANEMA_RESOURCE_ORIGINS=origin;
const delay=ms=>new Promise(r=>setTimeout(r,ms));const result={at:new Date().toISOString(),scope:'isolated exact media functions and original local MP4s, synthetic DOM; not builder/cart/storefront QA',samples:[],checks:[]};let browser;
try{browser=await puppeteer.launch();result.browser=await browser.version();for(const width of [390,1440])for(let run=0;run<(beforeOnly||extraOnly?1:3);run++)for(const version of versions){
 const context=await browser.createBrowserContext(),page=await context.newPage();await page.setViewport({width,height:844,isMobile:width===390,hasTouch:width===390,deviceScaleFactor:1});const c=await page.createCDPSession();await c.send('Emulation.setCPUThrottlingRate',{rate:width===390?4:1});await c.send('Network.enable');await c.send('Network.setCacheDisabled',{cacheDisabled:true});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(origin+'/'+version,{waitUntil:'load'});
 const check=(name,passed)=>result.checks.push({width,run,version,name,passed});
 if(extraOnly){
  await page.evaluate(()=>document.querySelector('.scc-vid').scrollIntoView());await page.waitForFunction(()=>!document.querySelector('video').paused);
  await page.focus('.scc-vid button');await page.keyboard.press('Enter');await page.waitForFunction(()=>!document.querySelector('video').paused&&!document.querySelector('video').muted);
  await page.evaluate(()=>window.scrollTo(0,0));await delay(350);
  check('first-manual-video-original-defect-or-fixed',await page.$eval('video',(v,version)=>v.paused===(version==='after'),version));
  // Existing unsupported-browser fallback remains usable by a manual gesture.
  await page.evaluateOnNewDocument(()=>{delete window.IntersectionObserver;});
  await page.reload({waitUntil:'load'});
  check('fallback-starts-without-observer',await page.evaluate(()=>!('IntersectionObserver' in window)&&document.querySelector('video').paused));
  await page.evaluate(()=>document.querySelector('.scc-vid').scrollIntoView());await page.focus('.scc-vid button');await page.keyboard.press('Enter');await page.waitForFunction(()=>!document.querySelector('video').paused);
  check('manual-fallback-without-intersection-observer',await page.$eval('video',v=>!v.paused&&!v.muted&&v.controls));check('no-errors',errors.length===0);
  result.samples.push({width,run,version,checks_only:'first manual offscreen and existing no-IO fallback',errors});await context.close();continue;
 }
 await page.evaluate(()=>document.querySelector('.scc-vid').scrollIntoView());await page.waitForFunction(()=>!document.querySelector('video').paused);
 check('first-autoplays-muted',await page.$eval('video',v=>v.muted&&v.loop));
 await page.evaluate(()=>document.querySelectorAll('.scc-vid')[1].scrollIntoView());await delay(180);
 check('second-does-not-autoplay',await page.$eval('.scc-vid:nth-child(2) video',v=>v.paused));
 await page.focus('.scc-vid:nth-child(2) button');await page.keyboard.press('Enter');await page.waitForFunction(()=>!document.querySelectorAll('video')[1].paused);
 check('manual-video-unmuted-controls',await page.$eval('.scc-vid:nth-child(2) video',v=>!v.muted&&v.controls&&!v.loop));
 check('other-video-stopped',await page.$eval('video',v=>v.paused));
 await page.evaluate(()=>window.scrollTo(0,0));await delay(250);
 const offscreen=await page.$eval('.scc-vid:nth-child(2) video',v=>({paused:v.paused,time:v.currentTime,offscreen:v.getBoundingClientRect().top>innerHeight,error:v.error?.code??null,frames:v.getVideoPlaybackQuality().totalVideoFrames}));await delay(650);
 const later=await page.$eval('.scc-vid:nth-child(2) video',v=>({paused:v.paused,time:v.currentTime,frames:v.getVideoPlaybackQuality().totalVideoFrames}));
 check('confirmed-offscreen',offscreen.offscreen);check('expected-original-defect-or-fixed',version==='before'?!later.paused&&later.time-offscreen.time>.3:later.paused&&Math.abs(later.time-offscreen.time)<.05);
 // Return and use the existing native controls/play gesture: no seek/reset for manual playback.
 await page.evaluate(()=>document.querySelectorAll('.scc-vid')[1].scrollIntoView());await page.focus('.scc-vid:nth-child(2) button');await page.keyboard.press('Enter');await page.waitForFunction(()=>!document.querySelectorAll('video')[1].paused);
 check('manual-replay-works',await page.$eval('.scc-vid:nth-child(2) video',v=>!v.paused&&!v.muted&&v.controls));check('no-errors',errors.length===0&&offscreen.error===null);
 result.samples.push({width,run,version,offscreen,later,offscreen_media_progress_s:later.time-offscreen.time,offscreen_decoded_frames:later.frames-offscreen.frames,errors});await context.close();
}}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
result.passed=result.checks.every(c=>c.passed);result.remote_requests=0;result.commercial_requests=requests.filter(r=>!['GET','HEAD'].includes(r.method));await fs.writeFile(path.join(out,beforeOnly?'builder-video-original-failure.json':extraOnly?'builder-video-additional.json':'builder-video-browser.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({passed:result.passed,samples:result.samples.length,checks:result.checks.length,failures:result.checks.filter(c=>!c.passed),progress:result.samples.map(s=>({width:s.width,version:s.version,progress:s.offscreen_media_progress_s,frames:s.offscreen_decoded_frames}))}));if(!result.passed)process.exitCode=1;
