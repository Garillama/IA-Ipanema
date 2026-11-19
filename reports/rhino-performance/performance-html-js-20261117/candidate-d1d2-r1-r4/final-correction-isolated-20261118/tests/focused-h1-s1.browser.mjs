import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import http from 'node:http';
import { createRequire } from 'node:module';

const root = new URL('../', import.meta.url);
const hero = await fs.readFile(new URL('candidate/sections/hero.tpl', root), 'utf8');
const image = await fs.readFile(new URL('candidate/snippets/image.tpl', root), 'utf8');
const css = await fs.readFile(new URL('tests/style-critical-excerpt.css', root), 'utf8');
const require = createRequire('/home/alanrichard/.local/lib/node_modules/@tiendanube/cli/package.json');
const puppeteer = require('puppeteer');

const checks = [];
function check(condition, label) {
  assert.ok(condition, label);
  checks.push(label);
}

const responsiveBranch = hero.split('{% if has_responsive_images %}')[1].split('{% elseif has_desktop_image %}')[0];
check(responsiveBranch.includes("image_classes: '',"), 'responsive branch has no LazySizes fade classes');
check(responsiveBranch.includes('image_lazy: not is_priority_section') && responsiveBranch.includes('image_lazy_js: false'), 'secondary responsive images use native lazy loading');
check(!/lazyload|fade-in|placeholder-fade/.test(responsiveBranch), 'responsive branch has no contradictory class or sibling placeholder');
check(image.includes('{% if image_lazy and not image_lazy_js %}\n\t\tloading="lazy"'), 'helper emits the native loading attribute for this contract');
check(image.includes('and not (has_art_direction and image_raw_url_valid)'), 'raw direct art-direction URLs do not receive fabricated width descriptors');
check(image.includes('media.srcSets if srcSet.format != \'original\''), 'valid platform AVIF/WebP sets remain emitted');
check(image.includes('media and srcset ? srcset : image_src'), 'platform original responsive set remains the desktop fallback');
check(image.includes('mobile_original_srcset ? mobile_original_srcset : image_mobile_src'), 'platform original responsive set remains the mobile fallback');
check(hero.includes('{% elseif has_mobile_image %}') && hero.includes('image_src: hero.image_mobile'), 'D1 mobile-only fallback remains present');
check(image.includes('image_source_invalid') && image.includes('and not image_source_invalid'), 'D2 unresolved media references remain suppressed');
check(image.includes('image_desktop_url_valid') && image.includes('mobile_source_url_valid'), 'R1/R4 art-direction validity gates remain present');
check(hero.includes('image_priority_high: is_priority_section'), 'first hero priority contract remains unchanged');

const requests = { mobile: 0, desktop: 0 };
const server = http.createServer((req, res) => {
  if (req.url === '/mobile.svg') {
    requests.mobile++;
    res.writeHead(200, { 'content-type': 'image/svg+xml', 'cache-control': 'no-store' });
    res.end('<svg xmlns="http://www.w3.org/2000/svg" width="820" height="1000"><rect width="100%" height="100%" fill="#345"/></svg>');
  } else if (req.url === '/desktop.svg') {
    requests.desktop++;
    res.writeHead(200, { 'content-type': 'image/svg+xml', 'cache-control': 'no-store' });
    res.end('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="900"><rect width="100%" height="100%" fill="#567"/></svg>');
  } else {
    res.writeHead(204);
    res.end();
  }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const { port } = server.address();
const origin = `http://127.0.0.1:${port}`;
const browser = await puppeteer.launch({ headless: true, args: ['--disable-dev-shm-usage'] });
const browserResults = [];

try {
  for (const viewport of [{ width: 412, height: 823, expected: 'mobile.svg' }, { width: 1440, height: 900, expected: 'desktop.svg' }]) {
    requests.mobile = 0;
    requests.desktop = 0;
    const page = await browser.newPage();
    await page.setViewport({ width: viewport.width, height: viewport.height, deviceScaleFactor: 1 });
    const markup = `<!doctype html><meta name="viewport" content="width=device-width, initial-scale=1"><style>${css}\nhtml,body{margin:0} .hero{min-height:50vh} picture{display:block;width:100%} img{display:block;width:100%;height:auto}</style><section class="hero"><picture><source media="(max-width: 767.98px)" srcset="${origin}/mobile.svg" sizes="100vw" width="820" height="1000"><source srcset="${origin}/desktop.svg" sizes="100vw" width="1920" height="900"><img src="${origin}/desktop.svg" width="1920" height="900" loading="lazy" sizes="100vw" alt="Mismo mensaje visual"></picture></section>`;
    await page.setContent(markup, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => {
      const img = document.querySelector('img');
      return img && img.complete && img.naturalWidth > 0;
    }, { timeout: 8000 });
    const state = await page.evaluate(() => {
      const img = document.querySelector('img');
      const section = document.querySelector('.hero');
      return {
        currentSrc: img.currentSrc,
        loading: img.loading,
        className: img.className,
        opacity: getComputedStyle(img).opacity,
        placeholders: document.querySelectorAll('.placeholder-fade').length,
        alt: img.alt,
        imageHeight: img.getBoundingClientRect().height,
        sectionHeight: section.getBoundingClientRect().height,
        layoutShifts: performance.getEntriesByType('layout-shift').filter(e => !e.hadRecentInput).map(e => e.value),
      };
    });
    assert.equal(state.currentSrc, `${origin}/${viewport.expected}`, `viewport ${viewport.width} selects only its matching source`);
    assert.equal(state.loading, 'lazy', `viewport ${viewport.width} keeps native lazy loading`);
    assert.equal(state.className, '', `viewport ${viewport.width} has no LazySizes/fade state classes`);
    assert.equal(state.opacity, '1', `viewport ${viewport.width} becomes visible without .lazyloaded`);
    assert.equal(state.placeholders, 0, `viewport ${viewport.width} has no persistent placeholder`);
    assert.equal(state.alt, 'Mismo mensaje visual', 'one shared alt describes the same visual message');
    assert.equal(requests.mobile + requests.desktop, 1, `viewport ${viewport.width} makes exactly one image request`);
    assert.equal(requests[viewport.expected === 'mobile.svg' ? 'mobile' : 'desktop'], 1);
    assert.ok(state.layoutShifts.reduce((sum, value) => sum + value, 0) <= 0.001, `viewport ${viewport.width} fixture layout shift stays within threshold`);
    browserResults.push({ viewport: viewport.width, ...state, requests: { ...requests } });
    await page.close();
  }
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}

console.log(JSON.stringify({
  kind: 'isolated-focused-h1-s1-browser-check',
  network: 'loopback-only synthetic SVG fixtures; no production or external requests',
  staticAssertions: checks.length,
  browserViewports: browserResults.length,
  checks,
  browserResults,
  limitation: 'This exercises representative emitted HTML/CSS in Chromium, not the Tiendanube Twig renderer or resolve_media implementation.',
}, null, 2));
