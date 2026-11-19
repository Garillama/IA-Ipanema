// Isolated reproduction of preload + static_inline contract, NOT a Tiendanube renderer.
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {puppeteer} from '../../../tools/browser_runtime.mjs';
const root='/home/alanrichard/Codefy/scentperfumesclaude';
const out=path.dirname(fileURLToPath(import.meta.url));
const critical=await fs.readFile(path.join(root,'static/css/style-critical.css'),'utf8');
const utilities=await fs.readFile(path.join(root,'static/css/style-utilities.css'),'utf8');
const baseline=await fs.readFile(path.join(root,'layouts/layout.tpl'),'utf8');
const candidate=await fs.readFile(new URL('../../../.local/scent-audit-20261118/layout-candidate.tpl',import.meta.url),'utf8');
if(!baseline.includes("'css/style-critical.css' | static_url | static_inline")||!baseline.includes("'css/style-utilities.css' | static_url | static_inline"))throw Error('Inline source contract changed');
const expected=baseline.split(/(?<=\n)/).filter(line=>!(line.includes('rel="preload"')&&['css/style-critical.css','css/style-utilities.css'].some(name=>line.includes(name)))).join('');
if(candidate!==expected)throw Error('Candidate differs from authorized two-line experiment');
const fixture=before=>`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">${before?'<link rel="preload" href="/critical.css" as="style"><link rel="preload" href="/utilities.css" as="style">':''}<style>${critical}</style><style>${utilities}</style></head><body><header><a href="#main">SCENT</a></header><main id="main"><h1>Perfumes originales</h1><p>Reproducción aislada de CSS inline y preload.</p><button type="button">Explorar perfumes</button><div style="width:240px;height:150px;background:#33483e"></div></main></body></html>`;
const server=http.createServer((req,res)=>{
 const file={'/critical.css':critical,'/utilities.css':utilities}[req.url];
 res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',file?'text/css':'text/html; charset=utf-8');res.end(file??fixture(req.url==='/before'));
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
process.env.IPANEMA_RESOURCE_ORIGINS=origin;
const results={kind:'isolated-browser-experiment',scope:'CSS preload/inline reproduction only; not full storefront or Lighthouse',source_bytes:Buffer.byteLength(critical)+Buffer.byteLength(utilities),samples:[],checks:[]};
let browser;
try{
 browser=await puppeteer.launch();results.browser=await browser.version();results.node=process.version;
 for(const width of [390,1440])for(const javascript of [true,false])for(let run=0;run<(javascript?3:1);run++){
  const pair=[];
  for(const version of ['before','after']){
   const context=await browser.createBrowserContext();const page=await context.newPage();await page.setViewport({width,height:844,isMobile:width===390,hasTouch:width===390,deviceScaleFactor:1});
   await page.setJavaScriptEnabled(javascript);const client=await page.createCDPSession();await client.send('Network.enable');await client.send('Network.setCacheDisabled',{cacheDisabled:true});await client.send('Emulation.setCPUThrottlingRate',{rate:width===390?4:1});
   const requests=[],cssIds=new Set(),completed=[];
   client.on('Network.requestWillBeSent',e=>{if(e.type==='Stylesheet'){cssIds.add(e.requestId);requests.push({url:new URL(e.request.url).pathname});}});
   client.on('Network.loadingFinished',e=>{if(cssIds.has(e.requestId))completed.push({encoded_bytes:e.encodedDataLength});});
   await page.goto(`${origin}/${version}`,{waitUntil:'networkidle0',timeout:20000});
   // CDP DOM evaluation is intentionally allowed even when page scripts are disabled.
   const styles=await page.evaluate(()=>['body','header','h1','p','button','main'].map(s=>{const e=document.querySelector(s),c=getComputedStyle(e),r=e.getBoundingClientRect();return{selector:s,color:c.color,font:c.font,display:c.display,margin:c.margin,width:r.width,height:r.height};}));
   const screenshot=`${version}-${width}-${javascript?'js':'nojs'}-${run}.png`;await page.screenshot({path:path.join(out,screenshot)});
   const sample={width,javascript,run,version,css_requests:requests.length,requested_css:requests,completed_css:completed.length,css_encoded_bytes:completed.reduce((sum,e)=>sum+e.encoded_bytes,0),screenshot,styles};results.samples.push(sample);pair.push(sample);await context.close();
  }
  const [before,after]=pair;
  for(const [name,passed] of [['before-requests-two-css',before.css_requests===2],['after-requests-no-css',after.css_requests===0],['before-completes-two-css-after-zero',before.completed_css===2&&after.completed_css===0],['computed-styles-equal',JSON.stringify(before.styles)===JSON.stringify(after.styles)]])results.checks.push({width,javascript,run,name,passed});
 }
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
results.passed=results.checks.every(c=>c.passed);await fs.writeFile(path.join(out,'css-preload-experiment.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify({passed:results.passed,samples:results.samples.length,checks:results.checks.length,bytes:results.source_bytes}));
if(!results.passed)process.exitCode=1;
