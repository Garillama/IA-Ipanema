// Offline replay of archived public markup with local navigation CSS/JS.
// This is not a Tiendanube Twig renderer or a live storefront audit.
import fs from 'node:fs/promises';
import path from 'node:path';
const run=path.resolve(process.argv[2]),theme=path.resolve(process.argv[3]);
const output=path.join(run,'browser');
process.env.IPANEMA_EVIDENCE_DIR=output;
process.env.IPANEMA_ALLOW_NETWORK='0';
delete process.env.IPANEMA_AUDIT_PASSWORD;
const {puppeteer}=await import('../../tools/browser_runtime.mjs');
const archived=await fs.readFile(new URL('../runs/damarbeauty/20261108T211919-initial-audit-b5d2317b/public-home-initial.html',import.meta.url),'utf8');
const oldCSS=await fs.readFile(path.join(run,'before/static/css/damar-navigation-desktop.css'),'utf8');
const newCSS=await fs.readFile(path.join(theme,'static/css/damar-navigation-desktop.css'),'utf8');
const mobileCSS=await fs.readFile(path.join(theme,'static/css/damar-navigation-mobile.css'),'utf8');
const scripts=await Promise.all(['desktop','mobile'].map(name=>fs.readFile(path.join(theme,`static/js/damar-navigation-${name}.js`),'utf8')));
const records=[];let inventory;
const browser=await puppeteer.launch();
try{
 const parser=await browser.newPage();
 const markup=await parser.evaluate(html=>{
  const doc=new DOMParser().parseFromString(html,'text/html');
  const desktop=doc.querySelector('[data-damar-desktop-nav]'),mobile=doc.querySelector('[data-damar-nav-mobile]');
  if(!desktop||!mobile)throw Error('Archived navigation not found.');
  const clean=root=>{for(const e of root.querySelectorAll('script,iframe,form'))e.remove();for(const e of root.querySelectorAll('[src],[srcset]')){e.removeAttribute('src');e.removeAttribute('srcset');}return root.outerHTML;};
  return {desktop:clean(desktop),mobile:clean(mobile)};
 },archived);
 inventory=await parser.evaluate(html=>{
  const doc=new DOMParser().parseFromString(html,'text/html');
  // Align archive to the already-restored local checkpoint (hidden logo H1 removed).
  doc.querySelector('#logo h1[style]')?.remove();
  const collect=()=>[...doc.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e=>({tag:e.tagName,text:e.innerHTML.replace(/<br\s*\/?\s*>/gi,' ').replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim()}));
  const before=collect();
  for(const e of doc.querySelectorAll('[data-damar-desktop-nav] h2,[data-damar-desktop-nav] h3,[data-damar-nav-mobile] h2,[data-damar-nav-mobile] h3')){
   const p=doc.createElement(e.id==='damar-mobile-menu-title'?'div':'p');p.innerHTML=e.innerHTML;e.replaceWith(p);
  }
  return {method:'Expected outline from historical HTML; not live or Twig-rendered',before,after:collect()};
 },archived);
 await parser.close();
 for(const width of [360,390,768,1024,1279,1280,1440,1920]){
  const states=[];
  for(const version of ['before','after']){
   const page=await browser.newPage();
   try{
    const cdp=await page.createCDPSession();await cdp.send('Network.enable');await cdp.send('Network.setBlockedURLs',{urls:['*']});
    await page.setViewport({width,height:900,deviceScaleFactor:1});
    await page.setContent(`<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; connect-src 'none'"><title>Offline navigation replay</title></head><body><header class="js-header">${markup.desktop}</header><div id="nav-hamburger" class="modal-show">${markup.mobile}</div><main><h1>Beauty que <br>vale el hype.</h1></main></body></html>`);
    if(version==='after')await page.evaluate(()=>{
     const swap=(selector,tag,cls)=>document.querySelectorAll(selector).forEach(e=>{const n=document.createElement(tag);for(const a of e.attributes)n.setAttribute(a.name,a.value);if(cls)n.classList.add(cls);n.innerHTML=e.innerHTML;e.replaceWith(n);});
     swap('.damar-mega-desktop__heading h2','p','damar-mega-desktop__panel-title');
     swap('.damar-mega-desktop__column h3','p','damar-mega-desktop__column-title');
     swap('.damar-mega-desktop__editorial h3','p','damar-mega-desktop__editorial-title');
     for(const p of document.querySelectorAll('.damar-mega-desktop__editorial p:not(.damar-mega-desktop__editorial-title)'))p.classList.add('damar-mega-desktop__editorial-copy');
     for(const col of document.querySelectorAll('.damar-mega-desktop__column'))col.querySelector('ul').setAttribute('aria-label',col.querySelector('.damar-mega-desktop__column-title').textContent);
     swap('#damar-mobile-menu-title','div');swap('.damar-nav-mobile__eyebrow','p');
    });
    await page.addStyleTag({content:`body{margin:0} ${version==='before'?oldCSS:newCSS}\n${mobileCSS}`});
    // Only replace the absent native modal transport in this isolated fixture.
    // Real drill-in, focus, keyboard and desktop behavior use the unmodified local JS.
    await page.addScriptTag({content:"document.addEventListener('click',e=>{if(e.target.closest('#nav-hamburger .js-modal-close-private'))document.querySelector('#nav-hamburger').classList.remove('modal-show');});"});
    for(const content of scripts)await page.addScriptTag({content});
    await new Promise(r=>setTimeout(r,60));
    const desktop=width>=1280;
    if(desktop){await page.focus('[data-damar-mega-trigger]');await page.keyboard.press('ArrowDown');}
    else await page.click('[data-damar-nav-target]');
    const measure=await page.evaluate(desktop=>{
     const root=document.querySelector(desktop?'[data-damar-desktop-nav]':'[data-damar-nav-mobile]');
     return {geometry:[...root.querySelectorAll('*')].map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return [r.x,r.y,r.width,r.height,s.display,s.color,s.fontFamily,s.fontSize,s.fontWeight,s.lineHeight,s.margin,s.padding];}),
      links:[...root.querySelectorAll('a[href]')].map(e=>[e.getAttribute('href'),e.textContent]),
      headings:root.querySelectorAll('h1,h2,h3,h4,h5,h6').length,
      labelled_lists:[...root.querySelectorAll('ul')].filter(e=>e.getAttribute('aria-label')).length,
      focused:desktop?!!document.activeElement.closest('[data-damar-mega-panel]'):document.activeElement.hasAttribute('data-damar-nav-back'),
      expanded:desktop?document.querySelector('[data-damar-mega-trigger]').getAttribute('aria-expanded')==='true':root.dataset.damarNavState!=='main',
      named_dialog:desktop?null:document.querySelector('#nav-hamburger').getAttribute('aria-labelledby')==='damar-mobile-menu-title'&&!!document.getElementById('damar-mobile-menu-title')};
    },desktop);
    await page.screenshot({path:path.join(output,`${width}-${version}.png`)});
    if(!desktop){await page.click('[data-damar-nav-back]');measure.back=await page.evaluate(()=>document.querySelector('[data-damar-nav-mobile]').dataset.damarNavState==='main'&&document.activeElement.hasAttribute('data-damar-nav-target'));}
    await page.keyboard.press('Escape');
    measure.escape=await page.evaluate(desktop=>desktop?document.querySelector('[data-damar-mega-trigger]').getAttribute('aria-expanded')==='false':!document.querySelector('#nav-hamburger').classList.contains('modal-show'),desktop);
    states.push({version,...measure});
   }finally{await page.close();}
  }
  const [a,b]=states;
  records.push({width,geometry_equal:JSON.stringify(a.geometry)===JSON.stringify(b.geometry),links_equal:JSON.stringify(a.links)===JSON.stringify(b.links),before_headings:a.headings,after_headings:b.headings,after_labelled_lists:b.labelled_lists,before_interactions:[a.focused,a.expanded,a.back??true,a.escape,a.named_dialog??true],after_interactions:[b.focused,b.expanded,b.back??true,b.escape,b.named_dialog??true]});
 }
}finally{
 await browser.close();await fs.writeFile(path.join(output,'heading-outline.json'),JSON.stringify(inventory,null,2));await fs.writeFile(path.join(output,'comparison.json'),JSON.stringify({method:'Offline historical markup replay with local CSS/JS, remote resources blocked; native mobile open/close transport stubbed. Not Twig rendering.',records},null,2));
}
if(records.length!==8||records.some(r=>!r.geometry_equal||!r.links_equal||r.after_headings!==0||r.after_interactions.some(v=>!v)))process.exitCode=1;
console.log(JSON.stringify({cases:records.length,geometry_equal:records.filter(r=>r.geometry_equal).length,all_interactions:records.every(r=>r.after_interactions.every(Boolean))}));
