#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {cliRequire as require,puppeteer,authenticate,evidenceRoot,assertUrl} from './browser_runtime.mjs';
const {default:lighthouse}=await import(require.resolve('lighthouse'));
const {default:desktopConfig}=await import(require.resolve('lighthouse/core/config/desktop-config.js'));
import {safeLighthouseReport} from './performance_evidence.mjs';
if(process.argv[2]==='--job'){
 const job=JSON.parse(await fs.readFile(process.argv[3],'utf8'));
 if(!['mobile','desktop'].includes(job.device)||!Number.isInteger(job.runs)||job.runs<1||job.runs>5)throw Error('Trabajo Lighthouse inválido');
 assertUrl(job.url);
 const samples=[];
 for(let index=0;index<job.runs;index++){
  const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
  try{
   const port=Number(new URL(browser.wsEndpoint()).port);
   const throttling=job.device==='mobile'?{rttMs:150,throughputKbps:1638.4,cpuSlowdownMultiplier:4,requestLatencyMs:562.5,downloadThroughputKbps:1474.56,uploadThroughputKbps:675}:{rttMs:40,throughputKbps:10240,cpuSlowdownMultiplier:1,requestLatencyMs:0,downloadThroughputKbps:0,uploadThroughputKbps:0};
   const result=await lighthouse(job.url,{port,output:'json',logLevel:'error',onlyCategories:job.categories,locale:job.locale,throttlingMethod:'simulate',throttling,disableStorageReset:false},job.device==='desktop'?desktopConfig:undefined);
   result.lhr.environment={...result.lhr.environment,hostUserAgent:await browser.userAgent(),actualBrowserVersion:await browser.version()};
   if(browser.__accessLimited)throw Error('access_limited_stop');
   for(const value of [result.lhr.requestedUrl,result.lhr.finalDisplayedUrl||result.lhr.finalUrl]){if(typeof value!=='string')throw Error('incomplete_response');assertUrl(value);}
   const safe=safeLighthouseReport(result.lhr);
   samples.push(safe);

  }finally{await browser.close();}
 }
 for(let index=0;index<samples.length;index++)await fs.writeFile(path.join(evidenceRoot,'sample-'+(index+1)+'.json'),JSON.stringify(samples[index],null,2),{flag:'wx'});
 await fs.writeFile(path.join(evidenceRoot,'samples.json'),JSON.stringify(samples,null,2),{flag:'wx'});
 console.log(JSON.stringify({samples:samples.length,source:'lighthouse_local'}));
}else{
const url=process.argv[2];
const prefix=process.argv[3]||'';
if(!/^[a-z0-9-]*$/.test(prefix))throw Error('Prefijo no válido');
if(!url||new URL(url).protocol!=='https:') throw Error('Indicar URL HTTPS autorizada.');
const out=path.resolve(`${evidenceRoot}/measurements/lighthouse`);
await fs.mkdir(out,{recursive:true});
for(const device of ['mobile','desktop']){
 const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
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

}
