// Browser controller for DevTools: reuse the existing read-only Puppeteer boundary.
import readline from 'node:readline';
import {puppeteer,assertUrl} from './browser_runtime.mjs';

const browser=await puppeteer.launch();
const pages=new Map();let sequence=0;
process.stdout.write(JSON.stringify({endpoint:browser.wsEndpoint(),version:await browser.version()})+'\n');
const input=readline.createInterface({input:process.stdin});
try{
 for await(const line of input){
  let id=null;
  try{
   if(line.length>10000)throw Error('oversize');
   const request=JSON.parse(line);id=request.id;
   if(request.operation!=='open')throw Error('unsupported_operation');
   assertUrl(request.url);
   const page=(await browser.pages())[0];
   const response=await page.goto(request.url,{waitUntil:'domcontentloaded',timeout:30000});
   if([403,429].includes(response?.status()))throw Error('access_limited');
   pages.set(++sequence,page);
   process.stdout.write(JSON.stringify({id,result:{url:page.url(),status:response.status()}})+'\n');
  }catch{
   process.stdout.write(JSON.stringify({id,error:browser.__accessLimited===403?'forbidden_stop':browser.__accessLimited===429?'quota_stop':'browser_operation_failed'})+'\n');
  }
 }
}finally{await browser.close();}
