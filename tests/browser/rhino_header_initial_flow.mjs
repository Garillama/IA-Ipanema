/** Observable regression test for RHINO's initial header cascade.
 * Usage: node tests/browser/rhino_header_initial_flow.mjs CSS_FILE NEW_OUTPUT_DIR
 * Local fixture only: no storefront requests, no commercial actions, no WCAG certificate.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
const [cssPath,outPath]=process.argv.slice(2);
if(!cssPath||!outPath)throw Error('Provide CSS file and a new evidence directory.');
const css=await fs.readFile(cssPath,'utf8');
Object.assign(process.env,{IPANEMA_PUBLIC_URL:'https://rhino-performance.com/',IPANEMA_ALLOWED_ORIGINS:'https://rhino-performance.com',IPANEMA_ALLOW_NETWORK:'0',IPANEMA_RESOURCE_ORIGINS:'https://127.0.0.1',IPANEMA_EVIDENCE_DIR:path.resolve(outPath)});
const {puppeteer}=await import('../../tools/browser_runtime.mjs');
const browser=await puppeteer.launch();const checks=[];let failure;
try{
 for(const scripts of [true,false]){
  const context=await browser.createBrowserContext(),page=await context.newPage();
  await page.setJavaScriptEnabled(scripts);
  for(const width of [360,390,768,1024,1440,1920]){
   await page.setViewport({width,height:900});
   for(const variant of ['eligible','not-home','disabled','runtime-set','not-first','not-video']){
    const headerClass=variant==='disabled'?'':'head-transparent-enabled';
    const runtime=variant==='runtime-set'?'data-transparent-runtime="false"':'';
    const bodyClass=variant==='not-home'?'template-product':'template-home';
    const intro=variant==='not-first'?'<section>Editorial</section>':'';
    const mediaClass=variant==='not-video'?'section-image':'section-video';
    await page.setContent(`<body class="${bodyClass}"><header><section class="section-header"><div class="head-main ${headerClass}" ${runtime}>Header</div></section></header><main id="MainContent">${intro}<section class="${mediaClass}"><div class="video-section-background">Media</div></section></main></body>`);
    await page.addStyleTag({content:css});
    const actual=await page.$eval('.head-main',e=>getComputedStyle(e).position);
    const expected=scripts&&width>=1024&&variant==='eligible'?'absolute':'static';
    checks.push({name:`initial-header-${width}-${scripts?'enabled':'disabled'}-${variant}`,status:actual===expected?'passed':'failed',actual,expected});
   }
  }
  await context.close();
 }
}catch(e){failure=e.message;}finally{await browser.close();}
const proof={kind:'qa',project:'rhino-performance',at:new Date().toISOString(),outcome:!failure&&checks.length===72&&checks.every(x=>x.status==='passed')?'passed':'failed',checks,error:failure,verification_state:{theme:{'static/css/style-critical.css':crypto.createHash('sha256').update(css).digest('hex')}},scope:'72 actual Chrome computed-style assertions; native CSS/JS-disabled media behavior in local fixture, not remote Twig rendering or full accessibility/commerce.'};
await fs.writeFile(path.join(outPath,'qa.json'),JSON.stringify(proof,null,2),{flag:'wx'});
console.log(JSON.stringify({outcome:proof.outcome,checks:checks.length,failed:checks.filter(x=>x.status==='failed')}));
process.exitCode=proof.outcome==='passed'?0:1;
