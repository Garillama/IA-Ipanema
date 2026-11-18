import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const candidateRoot = new URL('../', import.meta.url);
const themeRoot = process.env.IPANEMA_THEME_ROOT || new URL('../', import.meta.url).pathname;
const heroTpl = await fs.readFile(`${themeRoot}/sections/hero.tpl`, 'utf8');
const imageTpl = await fs.readFile(`${themeRoot}/snippets/image.tpl`, 'utf8');
const homeConfig = JSON.parse(await fs.readFile(`${themeRoot}/templates/pages/home.json`, 'utf8'));
const require = createRequire('/home/alanrichard/.local/lib/node_modules/@tiendanube/cli/package.json');
const puppeteer = require('puppeteer');
const library = await fs.readFile(`${themeRoot}/static/js/libraries-standalone.js`, 'utf8');
const lazyStart = library.indexOf('/*! lazysizes');
const lazyEnd = library.indexOf('/* Swiper 6.3.2 */');
if (lazyStart < 0 || lazyEnd <= lazyStart) throw new Error('No se localizó LazySizes empaquetado.');
const lazySizesSource = library.slice(lazyStart, lazyEnd);

const checks=[];
function check(value,label){assert.ok(value,label);checks.push(label);}
check(heroTpl.includes('desktop_media_url_valid') && heroTpl.includes('mobile_media_url_valid'), 'hero valida por separado ambas variantes y exige medio de imagen con URL HTTP(S)');
check(heroTpl.includes('matches \'#^https?://(?:[A-Za-z0-9]'), 'URL directa exige esquema y host con etiquetas válidas, no cualquier cadena');
check(heroTpl.includes('{% elseif has_mobile_image %}') && heroTpl.includes('image_src: hero.image_mobile'), 'si solo la imagen móvil es válida se usa como única imagen en ambos anchos');
check(heroTpl.includes('show_placeholder = not has_desktop_image and not has_mobile_image'), 'el placeholder de hero queda limitado al caso sin ninguna imagen válida');
check(imageTpl.includes('image_source_invalid') && imageTpl.includes('and not image_source_invalid'), 'el helper no renderiza referencias internas de medios sin resolver');
check(imageTpl.includes('mobile_media_url_valid') && imageTpl.includes('mobile_raw_url_valid'), 'la alternativa móvil distingue referencia resuelta de URL externa validada');
check(imageTpl.includes('image_raw_url_valid') && imageTpl.includes('image_source_invalid'), 'el helper rechaza texto arbitrario e identificadores internos no resueltos en art direction');
check(imageTpl.includes('mobile_original_srcset ? mobile_original_srcset : image_mobile_src'), 'fallback original móvil conserva srcset responsive cuando Tiendanube lo entrega');
check(imageTpl.includes('media and srcset ? srcset : image_src'), 'fallback original desktop conserva srcset responsive cuando Tiendanube lo entrega');
check(imageTpl.includes('srcSet.format != \'original\'') && imageTpl.includes('type="image/{{ srcSet.format }}"'), 'formatos AVIF/WebP siguen procediendo exclusivamente de srcSets');
check(imageTpl.includes('image_mobile_width') && imageTpl.includes('image_mobile_height') && imageTpl.includes('image_width') && imageTpl.includes('image_height'), 'dimensiones disponibles se conservan para sources y fallback');
check(heroTpl.includes('image_alt: image_mobile_alt'), 'hero solo móvil usa su texto alternativo propio');
const heroId=homeConfig.order.find(id=>homeConfig.sections[id]?.type==='hero');
check(homeConfig.order[0]===heroId, 'la hero existente permanece como primera sección; home.json no requiere cambio');

const widths=[360,390,412,767,768,1024,1440,1920];
const mediaQuery='(max-width: 767.98px)';
const URL_RE=/^https?:\/\/(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:\/|[?#]|$)/;
const candidates={
  desk:{type:'image',sourceUrl:'https://fixtures.invalid/desktop-1920.svg',sourceWidth:1920,sourceHeight:900,altText:'Hero',extension:'svg',srcSets:[{format:'original',baseUrl:'https://fixtures.invalid/desktop-',sizes:[{w:480},{w:1024},{w:1920}]}]},
  mob:{type:'image',sourceUrl:'https://fixtures.invalid/mobile-820.svg',sourceWidth:820,sourceHeight:1000,altText:'Hero móvil',extension:'svg',srcSets:[{format:'original',baseUrl:'https://fixtures.invalid/mobile-',sizes:[{w:320},{w:640},{w:820}]},{format:'webp',baseUrl:'https://fixtures.invalid/mobile-webp-',sizes:[{w:640},{w:820}]},{format:'avif',baseUrl:'https://fixtures.invalid/mobile-avif-',sizes:[{w:640},{w:820}]}]},
  video:{type:'video',sourceUrl:'https://fixtures.invalid/clip.mp4'},
};
const originalSet=m=>m?.srcSets?.find(x=>x.format==='original');
function srcset(m){const s=originalSet(m);return s?s.sizes.map(x=>`${s.baseUrl}${x.w}.svg ${x.w}w`).join(', '):m?.sourceUrl||'';}
function resolve(value){
  if(typeof value!=='string'||!value)return null;
  if(value.startsWith('@media-lib:')){const m=candidates[value.slice(11)];return m?.type==='image'&&URL_RE.test(m.sourceUrl)?{url:m.sourceUrl,media:m}:null;}
  return URL_RE.test(value)?{url:value,media:null}:null;
}
function choose({desktop='@media-lib:desk',mobile='@media-lib:mob',mobileEnabled=true,priority=false,later=false}){
  const d=resolve(desktop),m=mobileEnabled?resolve(mobile):null;
  if(d&&m)return {mode:'picture',desktop:d,mobile:m,alt:d.media?.altText||'Hero'};
  if(d)return {mode:'single',asset:d,alt:d.media?.altText||'Hero'};
  if(m)return {mode:'single',asset:m,alt:m.media?.altText||'Hero móvil'};
  return {mode:'placeholder',asset:{url:'https://fixtures.invalid/placeholder-1280.svg',media:null},alt:'Hero',priority:false};
}
function sourceRows(m,media,query=''){
  if(!media)return [{media:query,srcset:m.url}];
  const rows=[];
  for(const s of media.srcSets.filter(x=>x.format!=='original')){
    rows.push({media:query,type:`image/${s.format}`,srcset:s.sizes.map(x=>`${s.baseUrl}${x.w}.svg ${x.w}w`).join(', ')});
  }
  rows.push({media:query,srcset:srcset(media)});
  return rows;
}
function markup(choice,{priority=false,later=false}={}){
  const p=choice.mode==='picture';
  const rows=p?[...sourceRows(choice.mobile,choice.mobile.media,mediaQuery),...sourceRows(choice.desktop,choice.desktop.media)]:[];
  const image=p?choice.desktop:choice.asset;
  const ratio=image.media?.sourceWidth&&image.media?.sourceHeight?`${image.media.sourceWidth}/${image.media.sourceHeight}`:(image.url.includes('mobile')?'820/1000':image.url.includes('placeholder')?'1280/700':'1920/900');
  const width=image.media?.sourceWidth||Number(ratio.split('/')[0]);
  const height=image.media?.sourceHeight||Number(ratio.split('/')[1]);
  const sources=rows.map(s=>`<source ${s.media?`media="${s.media}"`:''} ${s.type?`type="${s.type}"`:''} srcset="${s.srcset}" sizes="100vw" ${s.media&&s.media.includes('max-width')?`width="${choice.mobile.media?.sourceWidth||820}" height="${choice.mobile.media?.sourceHeight||1000}"`:`width="${width}" height="${height}"`}>`).join('');
  const attrs=`alt="${choice.alt}"${priority&&choice.mode!=='placeholder'?' fetchpriority="high"':''}${later?' loading="lazy" class="lazyload fade-in"':''}`;
  const imgset=image.media?` srcset="${srcset(image.media)}" sizes="100vw"`:'';
  return p?`<picture>${sources}<img ${attrs} src="${image.url}"${imgset}></picture>`:`<picture>${image.media?sourceRows(image,image.media).map(s=>`<source type="image/${s.type||'webp'}" srcset="${s.srcset}" sizes="100vw">`).join(''):''}<img ${attrs} src="${image.url}"${imgset} width="${width}" height="${height}" style="aspect-ratio:${ratio}"></picture>`;
}
function svg(name){const [w,h]=name.includes('mobile')?[820,1000]:name.includes('placeholder')?[1280,700]:[1920,900];return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#2960c8"/></svg>`;}
async function browserCase(browser,{label,width,input,expected,priority=false,later=false}){
  const page=await browser.newPage();await page.setViewport({width,height:823,deviceScaleFactor:width===412?1.75:1});
  const requests=[];await page.setRequestInterception(true);
  page.on('request',req=>{const u=req.url();if(u.startsWith('https://fixtures.invalid/')){requests.push(u);const n=new URL(u).pathname.split('/').pop().replace(/\.(svg|jpg|webp)$/,'');req.respond({status:200,contentType:'image/svg+xml',body:svg(n)}).catch(()=>{});}else req.abort().catch(()=>{});});
  const choice=choose(input);const html=markup(choice,{priority,later});
  assert.ok(!/(?:src|srcset)="@media-lib:/.test(html),`${label}: no @media-lib token reaches src/srcset`);
  if(choice.mode==='picture'){
    assert.ok(html.includes('mobile-320.svg 320w'),`${label}: original mobile fallback retains native responsive descriptors`);
    assert.ok(html.includes('desktop-480.svg 480w'),`${label}: original desktop fallback retains native responsive descriptors`);
  }
  const observer='<script>window.shifts=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)window.shifts.push(e.value)})).observe({type:"layout-shift",buffered:true});</script>';
  await page.setContent(`<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0}picture,img{display:block;width:100%}img{height:auto;object-fit:cover}</style>${observer}<main>${html}</main>`,{waitUntil:'domcontentloaded'});
  if(later){await page.addScriptTag({content:lazySizesSource});await page.waitForFunction(()=>window.lazySizes?.loader);await page.evaluate(()=>window.lazySizes.loader.unveil(document.querySelector('picture img')));}
  await page.waitForFunction(()=>{const i=document.querySelector('picture img');return i?.complete&&i.naturalWidth>0;},{timeout:5000});
  const r=await page.evaluate(()=>{const i=document.querySelector('picture img');const b=i.getBoundingClientRect();return {src:i.currentSrc,alt:i.alt,fetchpriority:i.getAttribute('fetchpriority'),loading:i.getAttribute('loading'),width:b.width,height:b.height,shifts:window.shifts};});
  assert.ok(r.src.includes(expected),`${label} ${width}: currentSrc=${r.src}, expected=${expected}`);
  assert.equal(requests.length,1,`${label} ${width}: exactly one effective image request; got ${JSON.stringify(requests)}`);
  assert.equal(requests[0],r.src,`${label}: requested resource equals currentSrc`);
  assert.ok(!r.src.includes('@media-lib:'),`${label}: no invalid internal reference requested`);
  assert.equal(r.alt,choice.alt,`${label}: one alt matches selected content policy`);
  assert.ok(r.shifts.reduce((a,b)=>a+b,0)<=0.001,`${label}: fixture CLS ${r.shifts}`);
  if(priority)assert.equal(r.fetchpriority,'high',`${label}: only real hero image gets priority`);
  if(later){assert.equal(r.loading,'lazy');assert.ok(r.fetchpriority!=='high');}
  await page.close();return {label,width,mode:choice.mode,currentSrc:r.src,requests:requests.length,ratio:Number((r.width/r.height).toFixed(4)),alt:r.alt,cls:r.shifts.reduce((a,b)=>a+b,0),priority:r.fetchpriority,loading:r.loading};
}

const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
const results=[];
try{
  for(const width of widths){const mobile=width<=767;
    results.push(await browserCase(browser,{label:'both',width,input:{},expected:mobile?'mobile-':'desktop-',priority:width===412}));
    results.push(await browserCase(browser,{label:'desktop-only',width,input:{mobileEnabled:false},expected:'desktop-'}));
    results.push(await browserCase(browser,{label:'mobile-only-D1',width,input:{desktop:null},expected:'mobile-'}));
  }
  for(const width of [412,767,768,1440,1920]){
    results.push(await browserCase(browser,{label:'unresolved-mobile-D2-desktop-survives',width,input:{mobile:'@media-lib:orphan'},expected:'desktop-'}));
    results.push(await browserCase(browser,{label:'unresolved-desktop-D2-mobile-survives',width,input:{desktop:'@media-lib:orphan'},expected:'mobile-'}));
    results.push(await browserCase(browser,{label:'video-desktop-R1-mobile-survives',width,input:{desktop:'@media-lib:video'},expected:'mobile-'}));
    results.push(await browserCase(browser,{label:'video-mobile-desktop-survives',width,input:{mobile:'@media-lib:video'},expected:'desktop-'}));
    results.push(await browserCase(browser,{label:'arbitrary-desktop-rejected-mobile-survives',width,input:{desktop:'javascript:alert(1)'},expected:'mobile-'}));
    results.push(await browserCase(browser,{label:'arbitrary-mobile-rejected-desktop-survives',width,input:{mobile:'not-an-image-url'},expected:'desktop-'}));
  }
  for(const width of [412,768,1440]){
    results.push(await browserCase(browser,{label:'none-placeholder',width,input:{desktop:null,mobile:'@media-lib:orphan'},expected:'placeholder-',priority:false}));
  }
  results.push(await browserCase(browser,{label:'first-priority-mobile-only',width:1440,input:{desktop:null},expected:'mobile-',priority:true}));
  results.push(await browserCase(browser,{label:'later-lazy-responsive',width:1440,input:{},expected:'desktop-',later:true}));
  results.push(await browserCase(browser,{label:'direct-absolute-url-accepted',width:1440,input:{desktop:'https://fixtures.invalid/custom-desktop.svg',mobileEnabled:false},expected:'custom-desktop'}));
}finally{await browser.close();}
const output={kind:'synthetic-browser-fallback-fixture',network:'only intercepted fixtures.invalid; no external network',widths,cases:results.length,sourceAssertions:checks.length,checks,results,limitations:['The harness models the validated template decision table and markup; it does not render Twig or execute Tiendanube resolve_media.','AVIF/WebP preservation is checked in template source and source-set data, not decoded from platform-served media.','Real renderer, lazy-load timing, visual editor, production currentSrc and Lighthouse remain pending.']};
await fs.writeFile(new URL('hero-responsive-fallback-results.json',candidateRoot),JSON.stringify(output,null,2));
console.log(JSON.stringify({kind:output.kind,cases:output.cases,sourceAssertions:output.sourceAssertions,results:output.results,limitations:output.limitations},null,2));
