#!/usr/bin/env node
import fs from 'node:fs/promises';
import {puppeteer,authenticate} from './browser_runtime.mjs';
const browser=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--disable-dev-shm-usage']});const results=[];
try{
 const cookies=await authenticate(browser,'https://rhinoipanema.mitiendanube.com/?exit_preview_theme_installation');
 for(const [name,url] of [['category','https://rhinoipanema.mitiendanube.com/productos/'],['pdp','https://rhinoipanema.mitiendanube.com/productos/botas-presoterapia-inalambricas-pro-air/']]){
  const ctx=await browser.createBrowserContext();await ctx.setCookie(...cookies);const p=await ctx.newPage();await p.setViewport({width:390,height:900,isMobile:true,hasTouch:true});await p.setJavaScriptEnabled(false);const response=await p.goto(url,{waitUntil:'networkidle2',timeout:40000});
  const dom=await p.evaluate(()=>({title:document.title,url:location.href,h1:[...document.querySelectorAll('h1')].map(e=>e.textContent.trim()),links:[...document.querySelectorAll('main a[href]')].map(e=>e.href),images:[...document.querySelectorAll('main img')].map(e=>({src:e.currentSrc,dataSrc:e.getAttribute('data-src'),dataSrcset:!!e.getAttribute('data-srcset'),opacity:getComputedStyle(e).opacity,display:getComputedStyle(e).display,loaded:e.naturalWidth>1})),asyncStylesheet:[...document.querySelectorAll('link[rel=stylesheet]')].map(e=>({href:e.href,media:e.media})),loadMore:[...document.querySelectorAll('.js-load-more a')].map(e=>({href:e.getAttribute('href'),text:e.textContent.trim()})),forms:[...document.querySelectorAll('main form')].map(e=>({method:e.method,action:e.action})),scrollWidth:document.documentElement.scrollWidth,innerWidth}));
  results.push({name,url,status:response.status(),verifiedAt:new Date().toISOString(),dom,limitations:['Inspección sin JS de página; no se envió el formulario de compra.','Las imágenes fuera de viewport pueden seguir pendientes por loading lazy nativo.']});await p.screenshot({path:`ipanema-discovery/13-evidence/screenshots/${name}-no-js-390.png`,fullPage:true});await ctx.close();
 }
}finally{await browser.close();await fs.writeFile('ipanema-discovery/13-evidence/measurements/browser/no-js-commerce.json',JSON.stringify(results,null,2));}
console.log(JSON.stringify(results.map(r=>({name:r.name,url:r.dom.url,images:r.dom.images.length,transparent:r.dom.images.filter(x=>x.opacity==='0').length,loadMore:r.dom.loadMore,async:r.dom.asyncStylesheet.filter(x=>x.media==='print').length}))));
