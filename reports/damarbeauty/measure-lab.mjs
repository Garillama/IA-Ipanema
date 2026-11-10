// Laboratorio de lectura; mismas protecciones de red que QA V2. No mide INP de campo.
import fs from 'node:fs/promises';
import path from 'node:path';
import {lighthouseEvidence} from '../../tools/performance_evidence.mjs';
const output=path.resolve(process.argv[2]);
const target=process.env.IPANEMA_PUBLIC_URL||'https://damarbeauty.mx/';
if(new URL(target).origin!=='https://damarbeauty.mx')throw Error('Origen distinto del proyecto Damar.');
process.env.IPANEMA_PUBLIC_URL=target;process.env.IPANEMA_ALLOWED_ORIGINS='https://damarbeauty.mx';process.env.IPANEMA_ALLOW_NETWORK='1';delete process.env.IPANEMA_AUDIT_PASSWORD;
const all=[];
for(const profile of ['mobile','desktop']){
 process.env.IPANEMA_EVIDENCE_DIR=path.join(output,profile);
 // Separate imports/processes required: the runtime caches its evidence destination.
 const {spawnSync}=await import('node:child_process');
 if(!process.argv[3]){
  const p=spawnSync(process.execPath,[import.meta.filename,output,profile],{encoding:'utf8',env:{...process.env,IPANEMA_EVIDENCE_DIR:path.join(output,profile)},timeout:180000});
  all.push({profile,exit:p.status,summary:p.stdout.trim(),error:p.stderr.slice(0,300)});continue;
 }
 if(profile!==process.argv[3])continue;
 const {puppeteer,loadDependency}=await import('../../tools/browser_runtime.mjs');
 const browser=await puppeteer.launch();
 try{
  const lighthouse=(await loadDependency('lighthouse')).default;
  const desktop=(await loadDependency('lighthouse/core/config/desktop-config.js')).default;
  const {lhr}=await lighthouse(target,{port:Number(new URL(browser.wsEndpoint()).port),output:'json',logLevel:'error',onlyCategories:['performance']},profile==='desktop'?desktop:undefined);
  if(browser.__accessLimited)throw Error('Acceso limitado; no reintentar.');
  const result={url:lhr.finalDisplayedUrl,profile,at:lhr.fetchTime,lighthouse_version:lhr.lighthouseVersion,config:lhr.configSettings,runtime_error:lhr.runtimeError||null,score:lhr.categories.performance.score,metrics:{lcp_ms:lhr.audits['largest-contentful-paint'].numericValue,cls:lhr.audits['cumulative-layout-shift'].numericValue,tbt_ms:lhr.audits['total-blocking-time'].numericValue,fcp_ms:lhr.audits['first-contentful-paint'].numericValue},field_inp:null,warnings:lhr.runWarnings,network_policy:'read-only-all-tabs-v1',performance_evidence:lighthouseEvidence(lhr)};
  await fs.mkdir(output,{recursive:true});await fs.writeFile(path.join(output,profile+'-metrics.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
 }finally{await browser.close();}
}
if(!process.argv[3]){await fs.mkdir(output,{recursive:true});await fs.writeFile(path.join(output,'execution.json'),JSON.stringify(all,null,2));console.log(JSON.stringify(all));}
