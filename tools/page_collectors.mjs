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
