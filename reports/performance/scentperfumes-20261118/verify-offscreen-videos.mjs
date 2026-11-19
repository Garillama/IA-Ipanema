// Reproduction of native autoplay attributes with local existing MP4; no remote media.
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {puppeteer} from '../../../tools/browser_runtime.mjs';
const root='/home/alanrichard/Codefy/scentperfumesclaude';
const source=await fs.readFile(path.join(root,'snippets/scent/landing-prueba-primero.tpl'),'utf8');
const videos=[...source.matchAll(/<video\b[^>]*>[\s\S]*?<\/video>/g)].map(m=>m[0].replace(/src="[^"]+"/,'src="/sample.mp4"'));
if(videos.length!==2)throw Error('Source contract changed');
const media=await fs.readFile(path.join(root,'static/videos/sc-ugc-demo-ia.mp4'));
const html=`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Autoplay local reproduction</title><style>video{width:240px;height:200px;display:block}</style><div style="height:1000px">Espaciador: videos fuera de pantalla</div>${videos.join('')}<div style="height:1200px"></div>`;
const server=http.createServer((req,res)=>{res.setHeader('Content-Type',req.url==='/sample.mp4'?'video/mp4':'text/html');res.end(req.url==='/sample.mp4'?media:html);});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin=`http://127.0.0.1:${server.address().port}`;process.env.IPANEMA_RESOURCE_ORIGINS=origin;
let browser;const results={scope:'native video autoplay offscreen reproduction only; replacement local media, original attrs',samples:[],checks:[]};
try{browser=await puppeteer.launch();results.browser=await browser.version();for(const width of [390,1440]){
 const context=await browser.createBrowserContext(),page=await context.newPage();await page.setViewport({width,height:844,isMobile:width===390});await page.goto(origin,{waitUntil:'networkidle0'});
 for(const [phase,scroll] of [['initial-offscreen',0],['visible',1000],['after-scrolling-past',1800]]){
  await page.evaluate(y=>scrollTo(0,y),scroll);await page.evaluate(()=>new Promise(r=>setTimeout(r,1500)));
  const sample=await page.evaluate(()=>[...document.querySelectorAll('video')].map(v=>{const b=v.getBoundingClientRect();return{paused:v.paused,currentTime:v.currentTime,readyState:v.readyState,error:v.error?.code??null,autoplay:v.autoplay,loop:v.loop,preload:v.preload,offscreen:b.top>innerHeight||b.bottom<0};}));results.samples.push({width,phase,videos:sample});
 }
 results.checks.push({width,name:'local-media-decodes',passed:results.samples.filter(s=>s.width===width).every(s=>s.videos.every(v=>v.error===null&&v.readyState>0))});await context.close();
}}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
results.passed=results.checks.every(c=>c.passed);await fs.writeFile(path.join(path.dirname(fileURLToPath(import.meta.url)),'offscreen-video-experiment.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
