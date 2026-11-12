# Revisión independiente de candidato, sin permiso de integración

El propietario solicita conservar infinite nativo y diseño. No se cambia setting classic (60porpágina) ni se reescribeLS. No cambios remotos ni al tema. Los dos archivos originales se respaldaron desde producción14828608, tienda7400935 medianteCLI/APIguardados de sololectura; hashes locales iguales. Es un candidato temporal, no aplicado. El consejo previo completó su defensa pendiente con el mismo contexto/hash, pero sigue needs_evidence y no aprueba este nuevo diff.

Producción comprobada sin repetir:12IDs iniciales,14tras scroll,orden inicial conservado,sin duplicados. Se observó GET nativo /productos/page/2/ con results_only=true,limit12,status200. GET de esa ruta completa:HTML200,canonicalpropio,dosproductos encontenido principal. No se probóvalor Twig next_link en este candidato, ni filtros/orden/variantes/3páginas reales del catálogo. Tiendaactual14productos.

En producción el control.js-load-more a no tienehref,role,tabindex. LS oculta el control inicialmente y lo muestra cuando se rebasa el umbral. No se concluye que su estado oculto sea una infracción de foco. La primera página nativa sigue autoscroll. En páginasdirectas posteriores el init actual sale si no encuentra.js-load-more.

El candidato: href condicionala next_link ya calculado por código existente; ramas posteriores usan la navegación nativa existente; labels prev/next; tras inicializarLS evita navegación de clic principal para queel handlernativo hagaappend. En modificadores no previeneeldefault. Guarddata impide añadir el listener propio dosveces; no afirma haceridempotenteLS.

QAprevio:node--check aprobado. Aún no render Twig real,pruebas de browsercandidato,seisancho,teclado/filtros/semántica modificadores/rendimiento comparable. No declares que esas pruebasya se ejecutaron. Evalúa archivos consumidores, riesgos y alternativas más simples. Puedes pedir cambios o bloquear. Ningún modelo puede aprobar producción.

## Manifest
{
  "files": [
    {
      "path": "snippets/product-list/pagination.tpl",
      "before_sha256": "c715cc6c77d07dced5cdad6066785142c307b0f3ca3429cf88f5290cf7f2edc2",
      "candidate_sha256": "735504d24ca18df1db5f7de2408f7bfc815ec950aa7cb34cb3a09f947e804d87"
    },
    {
      "path": "static/js/store.js",
      "before_sha256": "29dea94e46cc1bb423ddde71a42d807f22c944f09465d70400728d7ae95b4718",
      "candidate_sha256": "6aa0e14d50f1842f6b1b410db3e4faad53d7d447db2a02698dc089ded067fe04"
    }
  ],
  "applied": false,
  "production_authorized": false,
  "status": "needs_review_and_tests",
  "known_open_conditions": [
    "Native next_link rendered value not yet observed",
    "Modifier click/default navigation semantics must be reviewed",
    "Filters and deeper catalog behavior not tested",
    "Real Twig render and comparable performance pending"
  ]
}

## Diff exacto
```diff
--- a/snippets/product-list/pagination.tpl
+++ b/snippets/product-list/pagination.tpl
@@ -7,10 +7,10 @@
 {# Page-part cursor first (variants as products), classic pagination as fallback #}
 {% set prev_link = prev_href ?: pages.previous %}
 {% set next_link = next_href ?: pages.next %}
-{% if infinite_scroll %}
+{% if infinite_scroll and pages.current == 1 %}
 	{% if pages.current == 1 and (not pages.is_last or page_next) %}
 		<div class="js-load-more pagination-load-more">
-			<a class="btn btn-primary">
+			<a {% if next_link %}href="{{ next_link }}"{% endif %} class="btn btn-primary">
 				{{ 'general.show_more_products' | t }}
 				<span class="js-load-more-spinner pagination-load-more-spinner" style="display:none;">
 					<svg class="icon-loading icon-inline"><use xlink:href="#spinner-third"/></svg>
@@ -24,7 +24,7 @@
 {% else %}
 	{% if pages.numbers or next_href or prev_href %}
 		<div class="pagination-nav">
-			<a {% if prev_link %}href="{{ prev_link }}"{% endif %} class="pagination-arrow pagination-arrow-prev {% if not prev_link %}opacity-30 disabled{% endif %}">
+			<a {% if prev_link %}href="{{ prev_link }}"{% endif %} aria-label="{{ 'general.previous' | t }}" class="pagination-arrow pagination-arrow-prev {% if not prev_link %}opacity-30 disabled{% endif %}">
 				<svg class="slider-arrow slider-arrow-prev icon-inline"><use xlink:href="#arrow-long"/></svg>
 			</a>
 			{% if pages.numbers and not (product_listing and store.has_variants_as_products) %}
@@ -38,7 +38,7 @@
 					<span>{{ pages.amount }}</span>
 				</div>
 			{% endif %}
-			<a {% if next_link %}href="{{ next_link }}"{% endif %} class="pagination-arrow {% if not next_link %}opacity-30 disabled{% endif %}">
+			<a {% if next_link %}href="{{ next_link }}"{% endif %} aria-label="{{ 'general.next' | t }}" class="pagination-arrow {% if not next_link %}opacity-30 disabled{% endif %}">
 				<svg class="slider-arrow icon-inline"><use xlink:href="#arrow-long"/></svg>
 			</a>
 		</div>
--- a/static/js/store.js
+++ b/static/js/store.js
@@ -1756,6 +1756,16 @@
         LS.productItemSlider({ pagination_type: 'fraction' });
       }
     });
+
+    // Preserve the native append handler; href remains the no-JavaScript fallback.
+    const loadMoreLink = loadMoreBtn.querySelector('a[href]');
+    if (loadMoreLink && !loadMoreLink.dataset.hybridScrollLinkBound) {
+      loadMoreLink.addEventListener('click', function(event) {
+        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
+        event.preventDefault();
+      });
+      loadMoreLink.dataset.hybridScrollLinkBound = 'true';
+    }
   }
 
   /**

```
## Función nativa publicada (lectura de producción)
```js
function(e){e=Object.assign({},{debounceRate:100,productGridSelector:"",spinnerSelector:"",loadMoreButtonSelector:"",hideWhileScrollingSelector:"",productsPerPage:9,productsBeforeLoadMoreButton:100,restoreScrollPosition:!1,afterLoaded:function(){},variantsAsProducts:!1},e);const t=(0,n.jQueryNuvem)(e.spinnerSelector),i=(0,n.jQueryNuvem)(e.productGridSelector),o=(0,n.jQueryNuvem)(e.loadMoreButtonSelector),a=(0,n.jQueryNuvem)(e.hideWhileScrollingSelector);if(t.hide(),o.hide(),0===i.length)return;let s=1,l=1;const u=[];let d=!1,p=!1,h=e.productsPerPage;const v=e=>{if(!e)return null;const t=String(e).split(":"),i=parseInt(t[0],10),n=parseInt(t[1],10);return isNaN(i)||isNaN(n)?null:{page:i,offset:n}};let m=e.variantsAsProducts?v(i.attr("data-vap-next")):null,f=0;const g=i.position().top,y=i.height(),_=LS.debounce((()=>{(function(){if(d||p)return!1;const e=window.pageYOffset,t=g+i.height();return e+2*y>=t})()&&(t.css("display","block"),j().then((e=>{S(e)})).catch((()=>b())).finally((()=>{d=!1,t.css("display","none")})))}),e.debounceRate);function w(){p=!1,window.addEventListener("scroll",_),a.hide()}function b(){p=!0,window.removeEventListener("scroll",_),a.show()}function j(){d=!0;const t={results_only:!0,limit:e.productsPerPage,theme:LS.theme.code,nube_sdk:window.nubeSDK?1:void 0};m?(s=m.page,t.page_offset=m.offset):(s++,e.variantsAsProducts&&(t.page_offset=void 0));let i=location.pathname;return i=-1===i.indexOf("/page/")?i.replace(/\/$/,"")+"/page/"+s+"/":i.replace(/\/page\/(\d+)/,"/page/"+s),r.default.get(i+N(t),"application/json").then((e=>e.json()))}function S(t,i){if(e.variantsAsProducts)return E(t,i),void e.afterLoaded.call();const n=parseInt(t.page);if(n>l+1)u[n]=t;else{E(t,i);for(let e=n+1;e<u.length&&u[e];e++)E(u[e],i),delete u[e];e.afterLoaded.call()}}function E(r,a){if(m=r.page_next?v(r.page_next.page+":"+r.page_next.offset):null,r.has_results){f++,a||(function(t){const i={mpage:t.page};e.variantsAsProducts&&(i.mchunks=f);const n=location.pathname+N(i);history.replaceState({},"",n)}(r),h+=e.productsPerPage),l++;const t=(0,n.jQueryNuvem)(r.html);i.append(t),(0,c.sendLocationUpdatedToNubeSDK)(r.html,r.nube_sdk_products)}r.has_next?!a&&h>e.productsBeforeLoadMoreButton&&function(){b(),h=0;const e=j();o.show(),o.one("click",(()=>{o.hide(),t.css("display","block"),e.then((e=>{S(e),w()})).catch((()=>b())).finally((()=>{d=!1,t.css("display","none")}))}))}():b()}function C(){const e=new URLSearchParams(location.search);return e.delete("mpage"),e.delete("mchunks"),e.sort(),"hybridScroll:scrollPosition:"+location.pathname+"?"+e.toString()}function T(){try{const e=JSON.parse(sessionStorage.getItem(C()));return e&&"number"==typeof e.y?e:null}catch(e){return null}}function k(t){const i=/^\d+$/.test(t.productId)?document.querySelector(e.productGridSelector).querySelector('[data-product-id="'+t.productId+'"]'):null;i?window.scrollTo(0,i.getBoundingClientRect().top+window.pageYOffset-t.productTop):window.scrollTo(0,t.y),history.scrollRestoration="auto"}function N(e){const t=Object.assign({},LS.encodeURIParams(LS.urlParams),e);let i=[];for(const e in t)void 0!==t[e]&&i.push(e+"="+t[e]);return i=i.join("&"),"?"+i}!function(){const t=LS.getUrlParams();if(!e.variantsAsProducts){if(t.mpage){const i=e.restoreScrollPosition?T():null,n=[];null!==i&&(history.scrollRestoration="manual");for(let e=2;e<=t.mpage;e++)n.push(j().then((e=>{S(e,!0)})).catch((()=>b())).finally((()=>{d=!1})));null!==i&&Promise.all(n).then((()=>k(i)))}return}const i=Math.min(parseInt(t.mchunks,10)||(t.mpage?t.mpage-1:0),50);if(i>0){const t=e.restoreScrollPosition?T():null;null!==t&&(history.scrollRestoration="manual");const n=e=>e<=0||p?Promise.resolve():j().then((t=>(S(t,!0),d=!1,t.has_results&&t.has_next?n(e-1):Promise.resolve())));n(i).catch((()=>{b(),d=!1})).then((()=>{null!==t&&k(t)}))}}(),w(),e.restoreScrollPosition&&window.addEventListener("scroll",LS.debounce((function(){const t=function(){const t=document.querySelector(e.productGridSelector).querySelectorAll("[data-product-id]");let i=0,n=t.length-1,r=null;for(;i<=n;){const e=Math.floor((i+n)/2);t[e].getBoundingClientRect().bottom>0?(r=t[e],n=e-1):i=e+1}return r}(),i={y:Math.round(window.pageYOffset),productId:t?t.getAttribute("data-product-id"):null,productTop:t?Math.round(t.getBoundingClientRect().top):0};try{sessionStorage.setItem(C(),JSON.stringify(i))}catch(e){}}),e.debounceRate))}
```
## Footer e institucionales
La navegación nativa del footer usa menus[menu_id]. El bloqueMásinformación está configurado al menúfooter. ElHTMLcapturado traePrivacidad,Cambiosygarantía,Cookies,Envíos, pero no hrefaContacto niSobre. Ambos están en sitemap y dan200,canonicalpropio,H1,textopropio,sin meta/X-robotsrestrictivo observado. GSCContacto:descubiertasinindexar,Sobre:desconocida. Preferir agregar enlaces en menúfooter nativo si se confirma snapshotconfigrespaldo, antesde hardcodearnuevoslinks en tema. Causa algoritmoGoogle no conocida.

## Blog
Páginas2,3,8 conocidasenhrefs devuelven200,artículosdistintos,canonicala/blog/. GSCdesconocidas,sincanonicalGoogle. Head-tags escomponenteplataforma,documentaciónoficial no demuestraoverride. No hay candidato de canonical ni autorización de editarlo.
