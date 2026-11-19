// Actual theme scripts in an isolated empty-target fixture; not storefront INP.
import fs from 'node:fs/promises';import http from 'node:http';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {puppeteer} from '../../../../tools/browser_runtime.mjs';
const root='/home/alanrichard/Codefy/scentperfumesclaude';const names=['sc-global.js','sc-search-refinement.js'];const scripts=Object.fromEntries(await Promise.all(names.map(async name=>['/'+name,await fs.readFile(path.join(root,'static/js',name),'utf8')])));
const html='<!doctype html><html lang="es"><meta charset="utf-8"><title>Observer fixture</title><main><div id="unrelated"></div></main>'+names.map(n=>`<script src="/${n}" defer></script>`).join('')+'</html>';
const server=http.createServer((req,res)=>{res.setHeader('Content-Type',scripts[req.url]?'text/javascript':'text/html');res.end(scripts[req.url]??html);});await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;process.env.IPANEMA_RESOURCE_ORIGINS=origin;
let browser;const output={scope:'actual source scripts, unrelated mutation fixture; no navigation functionality or INP claim',samples:[]};
try{browser=await puppeteer.launch();output.browser=await browser.version();for(const width of [390,1440]){
 const context=await browser.createBrowserContext();const page=await context.newPage();await page.setViewport({width,height:844});const errors=[];page.on('pageerror',e=>errors.push(e.name));
 await page.evaluateOnNewDocument(()=>{window.fixtureScans={};const original=Document.prototype.querySelectorAll;Document.prototype.querySelectorAll=function(selector){if(['[data-sc-header]','[data-sc-search-refinement]'].includes(selector))window.fixtureScans[selector]=(window.fixtureScans[selector]||0)+1;return original.call(this,selector);};});
 await page.goto(origin,{waitUntil:'networkidle0'});
 const sample=await page.evaluate(async()=>{const before={...window.fixtureScans};const node=document.getElementById('unrelated');for(let i=0;i<20;i++){node.textContent=String(i);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));}return{before,after:{...window.fixtureScans},mutations:20};});output.samples.push({width,...sample,js_errors:errors});await context.close();
}}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
await fs.writeFile(path.join(path.dirname(fileURLToPath(import.meta.url)),'observer-scans.json'),JSON.stringify(output,null,2));console.log(JSON.stringify(output));
