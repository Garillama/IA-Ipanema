// Extraído de browser_audit V1; ambos runners comparten esta lectura.
export async function collectRendered(page){
return await page.evaluate(()=>({
      title:document.title,lang:document.documentElement.lang,bodyClass:document.body.className,
      viewport:{innerWidth,innerHeight,scrollWidth:document.documentElement.scrollWidth},
      headings:[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e=>({tag:e.tagName,text:e.textContent.trim()})),
      metadata:[...document.querySelectorAll('meta[name],meta[property],link[rel="canonical"],link[rel="alternate"]')].map(e=>({name:e.getAttribute('name')||e.getAttribute('property')||e.getAttribute('rel'),content:e.getAttribute('content'),href:e.getAttribute('href'),hreflang:e.getAttribute('hreflang')})),
      links:[...document.querySelectorAll('a[href]')].map(e=>({href:e.href,text:e.textContent.trim(),ariaLabel:e.getAttribute('aria-label')})),
      images:[...document.images].map(e=>({src:e.getAttribute('src'),currentSrc:e.currentSrc,srcset:e.getAttribute('srcset'),sizes:e.getAttribute('sizes'),alt:e.getAttribute('alt'),width:e.width,height:e.height,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight,loading:e.loading,fetchPriority:e.fetchPriority,display:getComputedStyle(e).display,visible:!!(e.getClientRects().length && e.getBoundingClientRect().bottom>0 && e.getBoundingClientRect().top<innerHeight)})),
      fonts:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status,display:f.display})),
      jsonld:[...document.querySelectorAll('script[type="application/ld+json"]')].map(e=>{try{return {component:e.dataset.component,value:JSON.parse(e.textContent)}}catch(err){return {error:String(err)}}}),
      navigation:performance.getEntriesByType('navigation').map(e=>e.toJSON()),
      paint:performance.getEntriesByType('paint').map(e=>e.toJSON()),
      performance:window.__audit||null,
      resources:performance.getEntriesByType('resource').map(e=>({name:e.name,initiatorType:e.initiatorType,transferSize:e.transferSize,encodedBodySize:e.encodedBodySize,decodedBodySize:e.decodedBodySize,duration:e.duration})),
      domNodes:document.getElementsByTagName('*').length,
      forms:[...document.forms].map(e=>({action:e.action,method:e.method,inputs:[...e.elements].map(x=>({tag:x.tagName,type:x.type,name:x.name,hasLabel:!!(x.labels&&x.labels.length),ariaLabel:x.getAttribute('aria-label')}))}))
    }));
}

// SEO projection only: never save cookies, inputs, execution scripts or data tokens.
// The initial response is parsed inertly. The live DOM is cloned before QA instrumentation.
export async function collectSEOProjection(page, initialHTML=null){
 return page.evaluate(html=>{
  const d=html===null?document.documentElement.cloneNode(true):new DOMParser().parseFromString(html,'text/html').documentElement;
  const secret=/password|cookie|authorization|access.?token|api.?key|secret|session|email|phone/i;
  const cleanURL=value=>{try{const u=new URL(value,location.href);if(u.username||u.password){u.username='';u.password='';}for(const key of [...u.searchParams.keys()])if(secret.test(key))u.searchParams.set(key,'[redacted]');return u.href;}catch{return value;}};
  let ldRedacted=false;
  const cleanData=value=>Array.isArray(value)?value.map(cleanData):value&&typeof value==='object'?Object.fromEntries(Object.entries(value).map(([k,v])=>{if(secret.test(k)){ldRedacted=true;return [k,'[redacted]'];}return [k,cleanData(v)];})):typeof value==='string'&&/^https?:/.test(value)&&/[?&](?:access_token|token|secret|password|session|email|phone|authorization)=/i.test(value)?(ldRedacted=true,cleanURL(value)):value;
  for(const e of d.querySelectorAll('input,textarea,select,iframe,object,embed'))e.remove();
  for(const e of d.querySelectorAll('script')){
   if(e.getAttribute('type')?.toLowerCase()!=='application/ld+json'){e.remove();continue;}
   // Keep normal JSON literal text: reserialization hides duplicate keys and can
   // round large numbers. Only redact when a known private field is detected.
   try{const before=ldRedacted;ldRedacted=false;const cleaned=cleanData(JSON.parse(e.textContent));if(ldRedacted)e.textContent=JSON.stringify(cleaned).replaceAll('<','\\u003c');ldRedacted=ldRedacted||before;}
   catch{e.textContent=e.textContent.replace(/("(?:password|access_token|secret|authorization)"\s*:\s*)"[^"\n]*"/gi,'$1"[redacted]"');}
  }
  for(const e of [d,...d.querySelectorAll('*')])for(const a of [...e.attributes]){
   const k=a.name.toLowerCase();
   if(secret.test(k)||k.startsWith('on')||k==='style'||k==='value'||k==='nonce'||k==='data-product-variants'){e.removeAttribute(a.name);continue;}
   if(['href','src','itemid','resource','about'].includes(k)&&a.value&&!a.value.startsWith('#'))e.setAttribute(k,cleanURL(a.value));
   else if(!(k==='type'&&e.tagName==='SCRIPT'||['id','class','lang','name','property','content','rel','href','src','alt','width','height','srcset','sizes','loading','fetchpriority','itemscope','itemtype','itemprop','itemid','itemref','typeof','vocab','prefix','resource','about','datatype','inlist','hreflang','role','aria-label'].includes(k)||k==='data-component'||k==='data-qa-carousel'))e.removeAttribute(a.name);
  }
  return {html:d.outerHTML,projection:'seo-public-markup-v2',json_ld_redacted:ldRedacted,limitations:['Proyección de HTML/DOM: elimina formularios, scripts ejecutables y atributos privados conocidos. No es copia íntegra de respuesta ni validador de privacidad universal.','JSON-LD conserva texto literal salvo redacción explícita de campos privados; revisar json_ld_redacted.','No infiere descargas de imágenes ni atribuye scripts a apps.']};
 },initialHTML);
}
