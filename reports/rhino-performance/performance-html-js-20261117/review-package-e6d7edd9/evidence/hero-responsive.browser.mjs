import fs from 'node:fs/promises';
import { createRequire } from 'node:module';

const themeRoot = process.env.IPANEMA_THEME_ROOT || '/home/alanrichard/Escritorio/Cli/Rhino-Ipanema';
const reportRoot = new URL('../', import.meta.url);
const require = createRequire('/home/alanrichard/.local/lib/node_modules/@tiendanube/cli/package.json');
const puppeteer = require('puppeteer');
const heroTpl = await fs.readFile(`${themeRoot}/sections/hero.tpl`, 'utf8');
const imageTpl = await fs.readFile(`${themeRoot}/snippets/image.tpl`, 'utf8');
const homeConfig = JSON.parse(await fs.readFile(`${themeRoot}/templates/pages/home.json`, 'utf8'));
const library = await fs.readFile(`${themeRoot}/static/js/libraries-standalone.js`, 'utf8');
const lazyStart = library.indexOf('/*! lazysizes');
const lazyEnd = library.indexOf('/* Swiper 6.3.2 */');
if (lazyStart < 0 || lazyEnd <= lazyStart) throw new Error('No se localizó la versión LazySizes empaquetada.');
const lazySizesSource = library.slice(lazyStart, lazyEnd);

const checks = [];
function assert(condition, message) {
  if (!condition) throw new Error(message);
  checks.push(message);
}

assert(heroTpl.includes('image_mobile_src: hero.image_mobile'), 'hero pasa la imagen móvil alternativa al helper');
const homeHeroId = homeConfig.order.find(id => homeConfig.sections[id]?.type === 'hero');
assert(!!homeHeroId && homeConfig.order[0] === homeHeroId, 'la instancia existente de hero sigue siendo la primera sección de home');
assert(heroTpl.includes('image_priority_high: is_priority_section'), 'solo la hero prioritaria recibe fetchpriority alto');
assert(heroTpl.includes('image_lazy: not is_priority_section') && heroTpl.includes('image_lazy_js: false'), 'variantes responsive no prioritarias usan loading nativo sin depender del loader para revelar srcsets');
assert(imageTpl.includes('media="{{ image_mobile_media_query | default(\'(max-width: 767.98px)\') }}"'), 'el helper acota art direction al mismo breakpoint que el layout');
assert(imageTpl.includes('{% if image_mobile_width %}width="{{ image_mobile_width }}"{% endif %}') && imageTpl.includes('{% if image_mobile_height %}height="{{ image_mobile_height }}"{% endif %}'), 'los source alternativos conservan dimensiones para proporción responsive');
assert(imageTpl.includes('{% if image_priority_high %}') && imageTpl.includes('fetchpriority="high"'), 'la prioridad sigue condicionada por image_priority_high');

const widths = [360, 390, 412, 768, 1024, 1440, 1920];
const mobileQuery = '(max-width: 767.98px)';
function imageSvg(name) { const [w,h] = name.includes('mobile') ? [820,1000] : (name.includes('placeholder') ? [1280,700] : [1920,900]); return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#2860cc"/></svg>`; }

function pictureMarkup({desktop=true, mobile=true, priority=false, lazy=false, placeholder=false}) {
  const attrs = `alt="Hero"${priority ? ' fetchpriority="high"' : ''}${lazy ? ' loading="lazy" class="lazyload fade-in"' : ''}`;
  const mobileSource = mobile ? `<source media="${mobileQuery}" srcset="https://fixtures.invalid/mobile.svg" width="820" height="1000">` : '';
  const fallback = desktop ? 'desktop' : (placeholder ? 'placeholder' : 'mobile');
  const src = fallback === 'desktop' ? 'desktop' : fallback;
  const desktopSource = `<source srcset="https://fixtures.invalid/${desktop ? 'desktop' : 'placeholder'}.svg" width="${desktop ? '1920' : '1280'}" height="${desktop ? '900' : '700'}">`;
  const selectedFallback = mobile && !desktop ? 'placeholder' : src;
  const fallbackUrl = `https://fixtures.invalid/${selectedFallback}.svg`;
  return `<picture>${mobileSource}${desktopSource}<img ${attrs} src="${fallbackUrl}"></picture>`;
}

async function runCase(browser, {label, width, dpr=1, markup, expected, lazy=false, spacer=false, expectedRatio=null}) {
  const page = await browser.newPage();
  await page.setViewport({width, height: 823, deviceScaleFactor:dpr});
  const requests = [];
  await page.setRequestInterception(true);
  page.on('request', req => {
    if (req.url().startsWith('https://fixtures.invalid/')) {
      requests.push(req.url());
      const name=new URL(req.url()).pathname.split('/').pop().replace('.svg','');
      req.respond({status:200, contentType:'image/svg+xml', body:imageSvg(name)}).catch(()=>{});
    } else req.abort().catch(()=>{});
  });
  const spacerMarkup = spacer ? '<div style="height:5000px"></div>' : '';
  const observer = `<script>window.__shifts=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)window.__shifts.push(e.value)})).observe({type:'layout-shift',buffered:true});</script>`;
  await page.setContent(`<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0}.hero{width:100%}picture,img{display:block;width:100%}img{height:auto;object-fit:cover}</style>${observer}</head><body>${spacerMarkup}<main class="hero">${markup}</main></body></html>`, {waitUntil:'domcontentloaded'});
  if (lazy) {
    await page.addScriptTag({content:lazySizesSource});
    await page.waitForFunction(() => window.lazySizes && window.lazySizes.loader);
    // Use the bundled LazySizes implementation to trigger the same opt-in lazy image path.
    await page.evaluate(() => { window.scrollTo(0, 5000); window.lazySizes.loader.unveil(document.querySelector('picture img')); });
  }
  await page.waitForFunction(() => {
    const img=document.querySelector('picture img');
    return img && img.complete && img.naturalWidth>0;
  }, {timeout:5000});
  const result = await page.evaluate(() => {
    const img=document.querySelector('picture img');
    const r=img.getBoundingClientRect();
    return {currentSrc:img.currentSrc, alt:img.alt, width:img.width, height:img.height, rect:{width:r.width,height:r.height}, fetchpriority:img.getAttribute('fetchpriority'), loading:img.getAttribute('loading'), shifts:window.__shifts};
  });
  const expectedUrl=`https://fixtures.invalid/${expected}.svg`;
  if (!result.currentSrc.includes(`/${expected}.svg`)) throw new Error(`${label} ${width}px: currentSrc ${result.currentSrc}, esperado ${expectedUrl}`);
  if (requests.length !== 1 || requests[0] !== result.currentSrc) throw new Error(`${label} ${width}px: requests=${JSON.stringify(requests)}, currentSrc=${result.currentSrc}`);
  if (result.alt !== 'Hero') throw new Error(`${label}: alt no preservado`);
  if (expectedRatio && Math.abs((result.rect.width/result.rect.height)-expectedRatio) > 0.02) throw new Error(`${label} ${width}px: ratio ${result.rect.width/result.rect.height} no coincide ${expectedRatio}`);
  if (result.shifts.reduce((a,b)=>a+b,0) > 0.001) throw new Error(`${label} ${width}px: CLS sintético ${result.shifts}`);
  if (label === 'first-priority' && result.fetchpriority !== 'high') throw new Error('La hero inicial no conserva fetchpriority=high');
  if (label === 'first-priority' && result.loading === 'lazy') throw new Error('La hero inicial quedó lazy');
  if (label === 'later-lazy' && result.loading !== 'lazy') throw new Error('La hero posterior no conserva loading=lazy');
  if (label === 'later-lazy' && result.fetchpriority === 'high') throw new Error('La hero posterior recibe prioridad alta indebidamente');
  await page.close();
  return {label,width,dpr,selected:expected,requestCount:requests.length,ratio:Number((result.rect.width/result.rect.height).toFixed(4)),fetchpriority:result.fetchpriority,loading:result.loading,cls:result.shifts.reduce((a,b)=>a+b,0)};
}

const browser=await puppeteer.launch({headless:true,args:['--disable-dev-shm-usage']});
const results=[];
try {
  for (const width of widths) {
    const mobile=width < 768;
    results.push(await runCase(browser,{label:'both-images',width,dpr:width===412?1.75:1,markup:pictureMarkup({}),expected:mobile?'mobile':'desktop',expectedRatio:mobile?0.82:1920/900}));
    results.push(await runCase(browser,{label:'desktop-only',width,markup:pictureMarkup({mobile:false}),expected:'desktop',expectedRatio:1920/900}));
    results.push(await runCase(browser,{label:'mobile-only',width,markup:pictureMarkup({desktop:false,mobile:true,placeholder:true}),expected:mobile?'mobile':'placeholder',expectedRatio:mobile?0.82:1280/700}));
    results.push(await runCase(browser,{label:'no-image-placeholder',width,markup:pictureMarkup({desktop:false,mobile:false,placeholder:true}),expected:'placeholder',expectedRatio:1280/700}));
  }
  for (const [width,dpr] of [[412,1.75],[1440,1]]) {
    results.push(await runCase(browser,{label:'first-priority',width,dpr,markup:pictureMarkup({priority:true}),expected:width<768?'mobile':'desktop',expectedRatio:width<768?0.82:1920/900}));
    results.push(await runCase(browser,{label:'later-lazy',width,dpr,markup:pictureMarkup({lazy:true}),expected:width<768?'mobile':'desktop',lazy:true,spacer:true,expectedRatio:width<768?0.82:1920/900}));
  }
} finally { await browser.close(); }
const output={kind:'synthetic-browser-fixture',network:'only intercepted fixture.invalid responses; no external network',widths,cases:results.length,assertions:checks.length+results.length*7,checks,results};
await fs.writeFile(new URL('hero-responsive-browser-results.json',reportRoot),JSON.stringify(output,null,2));
console.log(JSON.stringify(output,null,2));
