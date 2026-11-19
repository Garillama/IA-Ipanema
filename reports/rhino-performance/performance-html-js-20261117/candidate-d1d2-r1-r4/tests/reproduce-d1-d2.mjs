import fs from 'node:fs/promises';
import assert from 'node:assert/strict';

const prior = new URL('../../review-package-e6d7edd9/candidate/', import.meta.url);
const hero = await fs.readFile(new URL('sections/hero.tpl', prior), 'utf8');
const image = await fs.readFile(new URL('snippets/image.tpl', prior), 'utf8');

// D1: with a missing desktop image, the prior candidate explicitly substituted the placeholder.
assert.match(hero, /desktop_image\s*=\s*hero\.image\s*\?\s*hero\.image\s*:\s*\('images\/placeholders\/hero\/hero\.webp'/);
const d1 = { input: { desktop: null, mobile: '@media-lib:valid-mobile' }, priorDesktopSource: 'images/placeholders/hero/hero.webp', expected: 'mobile image at both viewport classes' };
assert.equal(d1.priorDesktopSource, 'images/placeholders/hero/hero.webp');

// D2: when the filter yields null, the old truthy reference still satisfied the art-direction guard.
assert.match(image, /not mobile_media or mobile_media\.type == 'image'/);
assert.match(image, /srcset="\{\{ image_mobile_src \}\}"/);
const d2 = { input: { mobile: '@media-lib:orphan', resolve_media: null }, priorGuard: Boolean('@media-lib:orphan') && (!null || null?.type === 'image'), priorMarkup: '<source srcset="@media-lib:orphan">', expected: 'reject internal ref and emit no invalid URL' };
assert.equal(d2.priorGuard, true);
assert.match(d2.priorMarkup, /srcset="@media-lib:/);

console.log(JSON.stringify({kind:'static-template-reproduction',network:'none',reproduced:['D1','D2'],limitations:['Source-level reproduction; no Tiendanube Twig renderer available.'],cases:[d1,d2]}, null, 2));
