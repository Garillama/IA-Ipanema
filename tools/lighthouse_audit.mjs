#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {cliRequire as require,puppeteer,authenticate} from './browser_runtime.mjs';
const {default:lighthouse}=await import(require.resolve('lighthouse'));
const {default:desktopConfig}=await import(require.resolve('lighthouse/core/config/desktop-config.js'));
const url=process.argv[2];
const prefix=process.argv[3]||'';
if(!/^[a-z0-9-]*$/.test(prefix))throw Error('Prefijo no válido');
if(!url||new URL(url).protocol!=='https:') throw Error('Indicar URL HTTPS autorizada.');
const out=path.resolve('ipanema-discovery/13-evidence/measurements/lighthouse');
await fs.mkdir(out,{recursive:true});
for(const device of ['mobile','desktop']){
 const browser=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--disable-dev-shm-usage']});
 try{
  const port=Number(new URL(browser.wsEndpoint()).port);
  const cookies=await authenticate(browser,url);
  if(cookies.length)await browser.defaultBrowserContext().setCookie(...cookies);
  const result=await lighthouse(url,{port,output:['json','html'],logLevel:'error',onlyCategories:['performance','accessibility','best-practices','seo']},device==='desktop'?desktopConfig:undefined);
  const lhr=result.lhr;
  await fs.writeFile(path.join(out,prefix+device+'.json'),JSON.stringify(lhr,null,2));
  await fs.writeFile(path.join(out,prefix+device+'.html'),result.report[1]);
  const summary={device,requestedUrl:lhr.requestedUrl,finalDisplayedUrl:lhr.finalDisplayedUrl,fetchTime:lhr.fetchTime,lighthouseVersion:lhr.lighthouseVersion,configSettings:lhr.configSettings,categories:Object.fromEntries(Object.entries(lhr.categories).map(([k,v])=>[k,v.score])),metrics:Object.fromEntries(['first-contentful-paint','largest-contentful-paint','cumulative-layout-shift','total-blocking-time','speed-index','server-response-time'].map(id=>[id,lhr.audits[id]?.numericValue])),warnings:lhr.runWarnings,runtimeError:lhr.runtimeError};
  await fs.writeFile(path.join(out,prefix+device+'-summary.json'),JSON.stringify(summary,null,2));
  console.log(JSON.stringify(summary));
 }finally{await browser.close();}
}
