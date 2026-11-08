#!/usr/bin/env node
import fs from 'node:fs/promises';
import {puppeteer,authenticate,evidenceRoot,assertUrl} from './browser_runtime.mjs';
const url=process.argv[2];if(!url)throw Error('URL autorizada necesaria.');assertUrl(url);
const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
try{
 const cookies=await authenticate(browser,url);const ctx=await browser.createBrowserContext();if(cookies.length)await ctx.setCookie(...cookies);
 const page=await ctx.newPage();await page.setViewport({width:1440,height:1000});const res=await page.goto(url,{waitUntil:'networkidle2',timeout:45000});
 const sample=await page.evaluate(()=>({title:document.title,url:location.href,bodyClass:document.body.className,headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>({tag:e.tagName,text:e.textContent.trim()})),links:[...document.querySelectorAll('a[href]')].map(e=>({href:e.href,text:e.textContent.trim(),label:e.getAttribute('aria-label')})),forms:[...document.forms].map(e=>({action:e.action,method:e.method,fields:[...e.elements].map(x=>({name:x.name,type:x.type}))})),sections:[...document.querySelectorAll('[data-section-type]')].map(e=>({id:e.id,type:e.dataset.sectionType,rect:{height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width}})),scripts:[...document.scripts].map(e=>e.src).filter(Boolean),metadata:[...document.querySelectorAll('meta[name],link[rel=canonical]')].map(e=>({name:e.getAttribute('name')||e.getAttribute('rel'),content:e.content,href:e.href})),text:document.body.innerText.slice(0,12000)}));
 const data={verifiedAt:new Date().toISOString(),status:res.status(),access:!!cookies.length,sample};await fs.writeFile(`${evidenceRoot}/measurements/browser/storefront-discovery.json`,JSON.stringify(data,null,2));
 await page.screenshot({path:`${evidenceRoot}/screenshots/storefront-discovery.png`,fullPage:true});
 console.log(JSON.stringify({status:data.status,url:sample.url,title:sample.title,sections:sample.sections,links:[...new Set(sample.links.map(x=>x.href))].filter(u=>u.startsWith(new URL(url).origin)),scripts:sample.scripts}));
}finally{await browser.close();}
