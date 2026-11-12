// Source-bound offline additions to the recorded RHINO review-layout QA.
// Tests count changes, API rendering and repeated calls without contacting the store.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

if (!process.argv[2] || !process.argv[3]) {
  throw Error('Uso: node tests/browser/rhino_review_edge_cases.mjs SNAPSHOT_RUN NUEVO_OUTPUT');
}
const sourceRun = path.resolve(process.argv[2]);
const output = path.resolve(process.argv[3]);
const supplement = process.argv.includes('--supplement');
await fs.mkdir(output, { recursive: true });
Object.assign(process.env, {
  IPANEMA_ALLOW_NETWORK: '0',
  IPANEMA_RESOURCE_ORIGINS: 'http://127.0.0.1',
  IPANEMA_EVIDENCE_DIR: path.join(output, 'browser'),
});
const { puppeteer } = await import('../../tools/browser_runtime.mjs');
const original = await fs.readFile(path.join(sourceRun, 'source/sections/google-reviews.tpl'), 'utf8');
const candidate = await fs.readFile(path.join(sourceRun, 'source/candidate/sections/google-reviews.tpl'), 'utf8');
const extract = text => ({
  script: text.match(/<script>([\s\S]*?)<\/script>/)[1],
  css: text.match(/<style>([\s\S]*?)<\/style>/)[1],
  fn: text.slice(text.indexOf('\t\tfunction setupMore() {'), text.indexOf('\n\t\tfunction updateArrows()')),
});
const versions = { baseline: extract(original), candidate: extract(candidate) };
const report = {
  at: new Date().toISOString(),
  project: 'rhino-performance',
  kind: 'offline_synthetic_browser_QA',
  source_hashes: Object.fromEntries(Object.entries({ original, candidate }).map(([k, v]) =>
    [k, crypto.createHash('sha256').update(v).digest('hex')])),
  checks: [],
  cases: [],
  limits: ['Synthetic review content is a test fixture, not actual merchant reviews.',
    'Source CSS with system font: validates logic and same-state geometry, not production typography.',
    'Repeated whole init is a baseline characterization, not a certification of component idempotency.'],
};
function check(id, value) {
  report.checks.push({ id, passed: Boolean(value) });
  if (!value) throw Error('Check failed: ' + id);
}
const longText = 'Texto largo sintético para comprobar truncamiento y controles. '.repeat(35);
function card(index, prefix = 'fixture') {
  return `<article class="hgr-carousel__card"><p id="${prefix}-${index}" class="hgr-carousel__text">${index % 2 ? 'Breve' : longText}</p><button type="button" class="hgr-carousel__more" aria-expanded="false" aria-controls="${prefix}-${index}">Leer más</button></article>`;
}
function body(count, api = false) {
  return `<section class="section-google-reviews" data-section-id="fixture-section"><div class="container google-reviews-container"><div class="hgr-carousel" data-hgr-carousel ${api ? 'data-hgr-api="https://fixture.invalid/reviews"' : ''} data-hgr-place-url="https://fixture.invalid/source"><div class="hgr-carousel__box"><div class="hgr-carousel__heading"><h2 class="hgr-carousel__title">Reseñas de prueba</h2><div class="hgr-carousel__heading-actions"><button type="button" class="hgr-carousel__arrow--prev" aria-label="Anterior">Anterior</button><button type="button" class="hgr-carousel__arrow--next" aria-label="Siguiente">Siguiente</button></div></div><div class="hgr-carousel__body"><div class="hgr-carousel__main"><div class="hgr-carousel__track" data-hgr-track>${Array.from({ length: count === 'blank' ? 1 : count }, (_, i) => card(i)).join('')}</div></div></div></div></div></div></section>`;
}
async function snapshot(page) {
  return page.evaluate(() => ({
    cards: [...document.querySelectorAll('.hgr-carousel__card')].map(e => {
      const t = e.querySelector('.hgr-carousel__text');
      const b = e.querySelector('.hgr-carousel__more');
      const box = e.getBoundingClientRect();
      return { more: e.classList.contains('has-more'), open: e.classList.contains('is-open'),
        width: box.width, height: box.height, textHeight: t?.clientHeight,
        expanded: b?.getAttribute('aria-expanded'), controls: b?.getAttribute('aria-controls'),
        targetExists: Boolean(document.getElementById(b?.getAttribute('aria-controls'))),
        buttonText: b?.textContent, buttonDisplay: b && getComputedStyle(b).display };
    }),
    arrows: [...document.querySelectorAll('.hgr-carousel__heading-actions button')].map(e => e.disabled),
  }));
}
let browser;
try {
  browser = await puppeteer.launch();
  report.chrome = await browser.version();
  for (const width of (supplement ? [390, 1440] : [390, 767, 768, 1023, 1024, 1440])) {
    for (const count of (supplement ? [3, 24] : [0, 1, 3, 5, 24, 100])) {
      const states = {};
      const repeatedMutations = {};
      for (const [variant, code] of Object.entries(versions)) {
        const page = await browser.newPage();
        await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
        await page.setContent(`<!doctype html><html lang="es"><head><style>body{margin:0;font-family:Arial}.container{max-width:1200px;margin:auto;padding:0 15px;box-sizing:border-box}${code.css}</style></head><body>${body(count)}</body></html>`);
        await page.addScriptTag({ content: code.script });
        await page.evaluate(fn => {
          const root = document.querySelector('[data-hgr-carousel]');
          window.__setupMore = new Function('root', fn + '; return setupMore;')(root);
        }, code.fn);
        const initial = await snapshot(page);
        repeatedMutations[variant] = await page.evaluate(async () => {
          let mutations = 0;
          const observer = new MutationObserver(rows => { mutations += rows.length; });
          observer.observe(document.querySelector('[data-hgr-carousel]'), { subtree: true, attributes: true, attributeFilter: ['class'] });
          for (let i = 0; i < 20; i++) window.__setupMore();
          await Promise.resolve();
          observer.disconnect();
          return mutations;
        });
        const repeated = await snapshot(page);
        check(`idempotent-state:${width}:${count}:${variant}`, JSON.stringify(initial) === JSON.stringify(repeated));
        if (variant === 'candidate') check(`no-redundant-class-writes:${width}:${count}`, repeatedMutations[variant] === 0);
        // Exercise dynamic replacement of the cards, as done by the existing renderer.
        await page.evaluate(({ short, long }) => {
          const track = document.querySelector('[data-hgr-track]');
          track.innerHTML = short + long;
          window.__setupMore();
          dispatchEvent(new Event('resize'));
          dispatchEvent(new Event('load'));
        }, { short: card(1, 'new'), long: card(0, 'new') });
        const replaced = await snapshot(page);
        const button = await page.$('.hgr-carousel__card.has-more .hgr-carousel__more');
        check(`long-control-present:${width}:${count}:${variant}`, Boolean(button));
        await button.focus();
        await page.keyboard.press('Enter');
        const opened = await snapshot(page);
        check(`keyboard-expanded:${width}:${count}:${variant}`, opened.cards[1].open && opened.cards[1].expanded === 'true');
        await page.evaluate(() => { dispatchEvent(new Event('resize')); window.__setupMore(); });
        const openAfterResize = await snapshot(page);
        check(`open-resize-state:${width}:${count}:${variant}`, JSON.stringify(opened) === JSON.stringify(openAfterResize));
        check(`open-focus-preserved:${width}:${count}:${variant}`, await button.evaluate(e => document.activeElement === e));
        await page.keyboard.press('Space');
        const closed = await snapshot(page);
        check(`keyboard-collapsed:${width}:${count}:${variant}`, !closed.cards[1].open && closed.cards[1].expanded === 'false');
        // Existing init has no guard: a second whole-script execution duplicates click listeners.
        await page.addScriptTag({ content: code.script });
        await button.focus();
        await page.keyboard.press('Enter');
        const duplicateInit = await snapshot(page);
        states[variant] = { initial, repeated, replaced, opened, closed, duplicateInit };
        await page.close();
      }
      check(`baseline-candidate-equivalent:${width}:${count}`, JSON.stringify(states.baseline) === JSON.stringify(states.candidate));
      report.cases.push({ width, count, repeatedMutations,
        duplicateInit: { baselineOpen: states.baseline.duplicateInit.cards[1].open,
          candidateOpen: states.candidate.duplicateInit.cards[1].open,
          characterization: 'Both retain baseline double-toggle; no new init listener or guard in this patch.' } });
    }
  }
  // Exercise the actual renderer/fetch path using an explicit offline fixture response.
  for (const count of [0, 1, 24, 'blank']) {
    const states = {};
    for (const [variant, code] of Object.entries(versions)) {
      const page = await browser.newPage();
      await page.setViewport({ width: 390, height: 900 });
      await page.setContent(`<!doctype html><html lang="es"><head><style>body{margin:0;font-family:Arial}${code.css}</style></head><body>${body(5, true)}</body></html>`);
      await page.evaluate(({ count, longText }) => {
        window.__mockCalls = 0;
        window.fetch = async () => {
          window.__mockCalls++;
          return { json: async () => ({ data: { reviews: { data: Array.from({ length: count === 'blank' ? 1 : count }, (_, i) => ({
            name: 'Autor sintético', rating: 4, review_created_at_date: '2026-01-01',
            content: { review_text: count === 'blank' ? '   ' : (i % 2 ? 'Breve' : longText) },
          })) }, source: { reviews_count: count } } }) };
        };
      }, { count, longText });
      await page.addScriptTag({ content: code.script });
      await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 0)));
      states[variant] = { snapshot: await snapshot(page), calls: await page.evaluate(() => window.__mockCalls) };
      check(`one-mocked-fetch:${count}:${variant}`, states[variant].calls === 1);
      check(`rendered-count:${count}:${variant}`, states[variant].snapshot.cards.length === (count === 'blank' ? 5 : count || 5));
      const control = await page.$('.hgr-carousel__card.has-more .hgr-carousel__more');
      check(`API-control:${count}:${variant}`, Boolean(control));
      await control.focus();
      await page.keyboard.press('Enter');
      check(`API-enter-aria:${count}:${variant}`, await control.evaluate(e => e.getAttribute('aria-expanded') === 'true' && e.closest('article').classList.contains('is-open')));
      check(`API-controls-target:${count}:${variant}`, await control.evaluate(e => Boolean(document.getElementById(e.getAttribute('aria-controls')))));
      await page.keyboard.press('Space');
      check(`API-space-aria-focus:${count}:${variant}`, await control.evaluate(e => e.getAttribute('aria-expanded') === 'false' && !e.closest('article').classList.contains('is-open') && document.activeElement === e));
      await page.close();
    }
    check(`API-render-equivalence:${count}`, JSON.stringify(states.baseline) === JSON.stringify(states.candidate));
  }
  report.status = 'passed';
} catch (error) {
  report.status = 'failed';
  report.error = error.message;
} finally {
  if (browser) await browser.close();
  await fs.writeFile(path.join(output, 'edge-qa.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ status: report.status, error: report.error, checks: report.checks.length, cases: report.cases.length }));
}
