// Offline browser QA of source-bound opt-in media. No Twig renderer or live API claim.
// node tests/browser/rhino_sectionfy_media.mjs CANDIDATE NEW_OUTPUT THEME_ASSETS
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
const [candidateArg,outputArg,themeArg]=process.argv.slice(2);
if(!candidateArg||!outputArg||!themeArg)throw Error('Indicar candidato, destino nuevo y assets del tema.');
const candidate=path.resolve(candidateArg),out=path.resolve(outputArg),theme=path.resolve(themeArg);
const homeOnly=process.argv.includes('--home-only');
await fs.mkdir(out,{recursive:true});
Object.assign(process.env,{IPANEMA_EVIDENCE_DIR:path.join(out,'browser'),IPANEMA_ALLOW_NETWORK:'0'});
const {puppeteer,cliRequire}=await import('../../tools/browser_runtime.mjs');
const read=name=>fs.readFile(path.join(candidate,name),'utf8');
const client=await read('static/js/sectionfy-client.js'),renderer=await read('static/js/sectionfy-video-slide.js');
const store=await read('static/js/store.js');
function sourceFunction(name){const begin=store.indexOf('  function '+name+'(');if(begin<0)throw Error(name);const end=store.indexOf('\n  function ',begin+5);return store.slice(begin,end<0?undefined:end);}
const initCode='var mobileInteracted=false;'+sourceFunction('deferOnMobile')+sourceFunction('hideSingleBulletPagination')+sourceFunction('initSwipers')+'\ninitSwipers();';
const library=await fs.readFile(path.join(theme,'static/js/libraries-standalone.js'),'utf8');
const visibility=await fs.readFile(path.join(theme,'static/js/media-visibility.js'),'utf8');
const css=(await fs.readFile(path.join(theme,'static/css/style-critical.css'),'utf8'))+'\n'+await read('static/css/sectionfy-video-slide.css');
const endpoint='https://api.bbeboy.store/api/public/video-banner/TEST_PUBLIC?placement=product&amp;target_id=fixture';
const img='data:image/svg+xml,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><rect width="600" height="400" fill="#555"/></svg>');
const ready={sections:{'video_banner-product-fixture-one':{estado:{lifecycle:'active',storefrontVisible:true},campos:{videoUrl:'https://cdn.example.com/fixture.mp4',videoMimeType:'video/mp4'},orden:0}}};
const report={at:new Date().toISOString(),scope:'Offline fixtures; real native Swiper and visibility helper, mocked API and media decoder/playback',checks:[],cases:[],network:false,theme_writes:false,hashes:{client:crypto.createHash('sha256').update(client).digest('hex'),renderer:crypto.createHash('sha256').update(renderer).digest('hex'),store:crypto.createHash('sha256').update(store).digest('hex')}};
function check(id,ok,details){report.checks.push({id,passed:!!ok,details});if(!ok)throw Error('Check failed: '+id);}
function slide(video=false,attrs=''){return '<div class="swiper-slide media" style="height:400px" '+(video?'data-sectionfy-kind="video_banner" data-sectionfy-video-slide data-sectionfy-video-endpoint="'+endpoint+'" data-sectionfy-token="TEST_PUBLIC" '+attrs:'')+'><div class="media-visual"><img src="'+img+'" width="600" height="400" alt="Foto de prueba"></div>'+(video?'<button type="button" class="sectionfy-video-toggle" data-sectionfy-video-toggle data-label-play="Reproducir video" data-label-pause="Pausar video" aria-label="Reproducir video" hidden><span data-sectionfy-video-play aria-hidden="true">▶</span><span data-sectionfy-video-pause aria-hidden="true" hidden>Ⅱ</span></button>':'')+'<a class="media-link" href="https://example.com/fixture" aria-label="Destino de prueba"></a></div>';}
let browser;
async function fixture(width=390,{payload=ready,status=200,video=true,attrs='',saveData=false,reduced=false,autoplay=false,standalone=false,pendingPlay=false,overlay=false,automaticHome=false}={}){
 const page=await browser.newPage();await page.setOfflineMode(true);await page.setViewport({width,height:900,isMobile:width<768,deviceScaleFactor:1});
 if(reduced)await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
 await page.setContent('<!doctype html><html lang="es"><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fixture RHINO</title><style>'+css+'\nbody{margin:0}.js-slideshow-container{width:100%;max-width:1440px}.swiper-container{width:100%;height:400px}</style></head><body><main><h1>Prueba de medios</h1><div class="js-slideshow-container"><div class="js-slideshow swiper-container" data-priority="true" data-autoplay="'+autoplay+'" data-speed="5000"><div class="swiper-wrapper">'+slide(video,attrs)+slide(false)+'</div><button type="button" class="js-swiper-slideshow-prev" aria-label="Anterior">Anterior</button><button type="button" class="js-swiper-slideshow-next" aria-label="Siguiente">Siguiente</button></div></div></main></body></html>');
 if(standalone){
  const bannerCSS=(await read('sections/video.tpl')).match(/<style>([\s\S]*?)<\/style>/)[1];
  await page.setContent('<!doctype html><html lang="es"><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Banner fixture</title><style>'+css+'\n'+bannerCSS+'\nbody{margin:0}</style></head><body><main><h1>Banner de prueba</h1><div class="js-video-section media media-full-width section-full-width video-section video-section-background video-section-custom-height video-section-custom-height-mobile" style="--video-custom-height:600px;--video-custom-height-mobile:340px" data-sectionfy-kind="video_banner" data-sectionfy-video-slide data-sectionfy-video-endpoint="'+endpoint+'" '+attrs+'><div class="media-visual"><img src="'+img+'" alt="Foto de prueba" width="600" height="400"></div><div class="video-controls-pills video-controls-align-right video-controls-valign-bottom" style="--video-controls-spacing-bottom:25px;--video-controls-scale:1;--video-controls-scale-mobile:1;--video-controls-bg:#000;--video-controls-bg-opacity:.7;--video-controls-color:#fff"><div class="container"><div class="video-controls-group"><span data-sectionfy-video-controls hidden><button type="button" class="js-video-section-playpause video-playpause-pill" data-sectionfy-video-toggle data-label-play="Reproducir video" data-label-pause="Pausar video" aria-label="Reproducir video"><svg data-sectionfy-video-play aria-hidden="true" width="20" height="20"><path d="M0 0L20 10L0 20Z"/></svg><svg data-sectionfy-video-pause aria-hidden="true" hidden width="20" height="20"><path d="M0 0h5v20h-5"/></svg></button></span></div></div></div><a class="media-link" href="https://example.com/fixture" aria-label="Destino de prueba"></a></div></main></body></html>');
 }
 if(automaticHome)await page.evaluate(()=>{const mount=document.querySelector('[data-sectionfy-video-slide]');mount.setAttribute('data-sectionfy-page','home-page');mount.setAttribute('data-sectionfy-video-endpoint','');});
 if(standalone&&overlay)await page.evaluate(()=>{
  const root=document.querySelector('[data-sectionfy-video-slide]');root.style.setProperty('--media-overlay-color','#000');root.style.setProperty('--media-overlay-opacity','0.4');
  const layer=document.createElement('div');layer.className='media-overlay';root.querySelector('.media-visual').appendChild(layer);
 });
 await page.evaluate(({payload,status,saveData,pendingPlay})=>{
  window.__calls=[];window.__plays=0;window.__paused=false;window.__hidden=false;
  Object.defineProperty(document,'hidden',{configurable:true,get:()=>window.__hidden});
  if(saveData)Object.defineProperty(navigator,'connection',{configurable:true,value:{saveData:true,addEventListener(){},removeEventListener(){}}});
  window.fetch=(url,options)=>{window.__calls.push({url:String(url).replace(/TEST_PUBLIC/g,'[fixture]'),credentials:options?.credentials,redirect:options?.redirect,cache:options?.cache});return Promise.resolve({ok:status===200,status,redirected:false,json:()=>Promise.resolve(payload)});};
  Object.defineProperty(HTMLMediaElement.prototype,'paused',{configurable:true,get(){return !this.__playing;}});
  HTMLMediaElement.prototype.play=function(){window.__plays++;if(pendingPlay)return new Promise(resolve=>{window.__finishPlay=()=>{this.__playing=true;this.dispatchEvent(new Event('playing'));resolve();};});this.__playing=true;this.dispatchEvent(new Event('playing'));return Promise.resolve();};
  HTMLMediaElement.prototype.pause=function(){const was=this.__playing;this.__playing=false;if(was)this.dispatchEvent(new Event('pause'));};
  HTMLMediaElement.prototype.load=function(){};
 },{payload,status,saveData,pendingPlay});
 await page.addScriptTag({content:library});await page.addScriptTag({content:visibility});await page.addScriptTag({content:client});await page.addScriptTag({content:renderer});
 if(!standalone){await page.addScriptTag({content:initCode});await page.waitForFunction(()=>!!document.querySelector('.js-slideshow').swiper);}
 await new Promise(r=>setTimeout(r,180));return page;
}
try{
 browser=await puppeteer.launch();report.chrome=await browser.version();
 if(!homeOnly){
 for(const width of[360,390,768,1024,1440,1920]){
  const p=await fixture(width);const state=await p.evaluate(()=>{const root=document.querySelector('[data-sectionfy-video-slide]'),v=root.querySelector('video'),sw=root.closest('.js-slideshow').swiper,b=root.querySelector('button');const r=b.getBoundingClientRect();return {video:!!v,src:v?.hasAttribute('src'),loop:sw.params.loop,buttonHidden:b.hidden,buttonTop:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('button')===b,overflow:document.documentElement.scrollWidth>innerWidth,requests:window.__calls.length};});
  check('video_prepared_'+width,state.video);check('manual_no_file_src_'+width,!state.src);check('one_request_'+width,state.requests===1);check('mixed_no_loop_'+width,!state.loop);check('control_above_link_'+width,state.buttonTop);check('no_overflow_'+width,!state.overflow);
  await p.focus('[data-sectionfy-video-toggle]');await p.keyboard.press('Enter');check('keyboard_play_'+width,await p.$eval('video',v=>!v.paused&&v.hasAttribute('src')));
  check('playing_label_'+width,await p.$eval('[data-sectionfy-video-toggle]',b=>b.getAttribute('aria-label')==='Pausar video'));
  await p.keyboard.press('Space');check('keyboard_pause_'+width,await p.$eval('video',v=>v.paused));
  await p.keyboard.press('Enter');await p.evaluate(()=>document.querySelector('.js-slideshow').swiper.slideTo(1,0));await new Promise(r=>setTimeout(r,130));check('pause_inactive_'+width,await p.$eval('video',v=>v.paused));
  check('inactive_control_not_tabstop_'+width,await p.$eval('[data-sectionfy-video-toggle]',b=>b.tabIndex===-1));
  check('focus_not_on_hidden_video_'+width,await p.$eval('[data-sectionfy-video-slide]',e=>!e.contains(document.activeElement)));
  if([390,1440].includes(width)){
   await p.evaluate(()=>document.querySelector('.js-slideshow').swiper.slideTo(0,0));await new Promise(r=>setTimeout(r,100));
   await p.addScriptTag({path:cliRequire.resolve('axe-core')});const axe=await p.evaluate(async()=>{const r=await window.axe.run('[data-sectionfy-video-slide]');return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})),incomplete:r.incomplete.map(v=>v.id)};});
   report.cases.push({width,axe});check('axe_media_'+width,axe.violations.length===0,axe.violations);
  }
  await p.screenshot({path:path.join(out,'media-'+width+'.png')});report.cases.push({width,state});await p.close();
 }
 const photos=await fixture(390,{video:false});check('photo_only_no_request',await photos.evaluate(()=>window.__calls.length===0));check('photo_only_loop_preserved',await photos.$eval('.js-slideshow',e=>e.swiper.params.loop===true));await photos.close();
 for(const [name,options]of Object.entries({null:{payload:{sections:{'video_banner-product-fixture-one':{estado:{lifecycle:'active',storefrontVisible:true},campos:{videoUrl:null,videoMimeType:null}}}}},hidden:{payload:{sections:{'video_banner-product-fixture-one':{...ready.sections['video_banner-product-fixture-one'],estado:{lifecycle:'active',storefrontVisible:false}}}}},http403:{status:403},http429:{status:429},bad_shape:{payload:{sections:[]}},ambiguous:{payload:{sections:{...ready.sections,'video_banner-product-fixture-two':ready.sections['video_banner-product-fixture-one']}}}})){
  const p=await fixture(390,options);check(name+'_poster',await p.$eval('.swiper-slide img',e=>e.complete&&e.naturalWidth>0));check(name+'_no_video',await p.evaluate(()=>document.querySelectorAll('video').length===0));check(name+'_one_request',await p.evaluate(()=>window.__calls.length===1));await p.addScriptTag({content:renderer});check(name+'_no_retry',await p.evaluate(()=>window.__calls.length===1));await p.close();
 }
 for(const mode of['mobile','saveData','reduced','desktop']){
  const p=await fixture(mode==='mobile'?390:1440,{attrs:'data-sectionfy-video-autoplay="true"',saveData:mode==='saveData',reduced:mode==='reduced'});check('auto_policy_'+mode,await p.$eval('video',(v,expected)=>v.hasAttribute('src')===expected,mode==='desktop'));await p.close();
 }
 const p=await fixture(1440);await p.focus('[data-sectionfy-video-toggle]');await p.keyboard.press('Enter');await p.evaluate(()=>{window.__hidden=true;document.dispatchEvent(new Event('visibilitychange'));});check('pause_hidden_tab',await p.$eval('video',v=>v.paused));await p.evaluate(()=>{window.__hidden=false;document.dispatchEvent(new Event('visibilitychange'));});await p.addScriptTag({content:client});await p.addScriptTag({content:renderer});check('duplicate_init_no_fetch',await p.evaluate(()=>window.__calls.length===1));
 await p.evaluate(()=>{window.__retainedVideo=document.querySelector('video');document.querySelector('.js-slideshow-container').remove();});await new Promise(r=>setTimeout(r,100));check('removed_video_released',await p.evaluate(()=>!window.__retainedVideo.hasAttribute('src')&&window.__retainedVideo.paused));await p.close();
 const security=await fixture(390,{video:false});const urls=['http://api.bbeboy.store/api/public/video-banner/T','https://evil.example/api/public/video-banner/T','https://user:pass@api.bbeboy.store/api/public/video-banner/T','https://api.bbeboy.store/admin/T','https://api.bbeboy.store:444/api/public/video-banner/T'];for(let i=0;i<urls.length;i++){const result=await security.evaluate(async url=>{try{await Sectionfy.loadVideoBanner(url);return false;}catch{return true;}},urls[i]);check('reject_endpoint_'+i,result);}check('rejected_endpoints_no_fetch',await security.evaluate(()=>window.__calls.length===0));await security.close();
 for(const width of[360,390,768,1024,1440,1920]){
  const p=await fixture(width,{standalone:true});const rect=await p.$eval('[data-sectionfy-video-slide]',e=>({width:e.offsetWidth,height:e.offsetHeight}));
  check('banner_no_initial_src_'+width,await p.$eval('video',v=>!v.hasAttribute('src')));
  check('banner_controls_visible_'+width,await p.$eval('[data-sectionfy-video-toggle]',e=>e.getBoundingClientRect().width>=40));
  await p.focus('[data-sectionfy-video-toggle]');await p.keyboard.press('Enter');check('banner_keyboard_play_'+width,await p.$eval('video',v=>!v.paused));
  check('banner_stable_dimensions_'+width,await p.$eval('[data-sectionfy-video-slide]',(e,r)=>e.offsetWidth===r.width&&e.offsetHeight===r.height,rect));
  await p.keyboard.press('Space');check('banner_keyboard_pause_'+width,await p.$eval('video',v=>v.paused));await p.screenshot({path:path.join(out,'banner-'+width+'.png')});await p.close();
 }
 const unavailable=await fixture(390,{standalone:true,status:403});check('banner_error_controls_hidden',await unavailable.$eval('[data-sectionfy-video-toggle]',e=>e.getBoundingClientRect().width===0));check('banner_error_no_video',await unavailable.evaluate(()=>!document.querySelector('video')));await unavailable.close();
 const flow=await fixture(1440,{autoplay:true});await flow.focus('[data-sectionfy-video-toggle]');await flow.keyboard.press('Enter');check('hold_slideshow_while_playing',await flow.$eval('.js-slideshow',e=>!e.swiper.autoplay.running));await flow.evaluate(()=>document.querySelector('.js-slideshow').swiper.slideTo(1,0));await new Promise(r=>setTimeout(r,200));await flow.evaluate(()=>document.activeElement.blur());await new Promise(r=>setTimeout(r,100));check('autoplay_photos_resumes',await flow.$eval('.js-slideshow',e=>e.swiper.autoplay.running));await flow.close();
 const exact=await fixture(390,{attrs:'data-sectionfy-video-key="video_banner-product-fixture-two"',payload:{sections:{...ready.sections,'video_banner-product-fixture-two':ready.sections['video_banner-product-fixture-one']}}});check('explicit_instance_works',await exact.evaluate(()=>!!document.querySelector('video')));await exact.close();
 const buffering=await fixture(1440,{autoplay:true,pendingPlay:true});await buffering.focus('[data-sectionfy-video-toggle]');await buffering.keyboard.press('Enter');await buffering.evaluate(()=>document.querySelector('.js-slideshow').swiper.autoplay.start());check('pending_video_holds_late_autoplay',await buffering.$eval('.js-slideshow',e=>!e.swiper.autoplay.running));await buffering.evaluate(()=>window.__finishPlay());check('pending_video_can_finish',await buffering.$eval('video',v=>!v.paused));await buffering.close();
 const layer=await fixture(1440,{standalone:true,overlay:true});check('banner_overlay_present',await layer.$eval('.media-overlay',e=>getComputedStyle(e).opacity==='0.4'));await layer.focus('[data-sectionfy-video-toggle]');await layer.keyboard.press('Enter');check('banner_overlay_above_video',await layer.$eval('.media-overlay',e=>Number(getComputedStyle(e).zIndex)>Number(getComputedStyle(e.parentElement.querySelector('video')).zIndex)));await layer.close();
 const noLayer=await fixture(1440,{standalone:true,overlay:false});check('banner_overlay_off',await noLayer.evaluate(()=>!document.querySelector('.media-overlay')));await noLayer.close();
 }
 const homeAuto=await fixture(390,{automaticHome:true});check('home_auto_source',await homeAuto.evaluate(()=>!!document.querySelector('video')));check('home_auto_endpoint',await homeAuto.evaluate(()=>window.__calls.length===1&&window.__calls[0].url==='https://sectionfy.codefy-apps.com/api/public/content/[fixture]/home-page'));await homeAuto.close();
 report.status='passed';
}catch(error){report.status='failed';report.error=error.message;}finally{if(browser)await browser.close();await fs.writeFile(path.join(out,'qa.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,error:report.error}));}
