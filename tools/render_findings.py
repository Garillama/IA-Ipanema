#!/usr/bin/env python3
"""Hallazgos revisados, enlazados a evidencia; propuestas, no correcciones instaladas."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'ipanema-discovery'
F=[]
def add(n,area,severity,status,title,evidence,current,recommendation,alternative,dependencies,risks,verify,reuse,scores):
    benefit,effort,risk,seo,perf,ux,shared,maint,platform=scores
    F.append(dict(id=f'IPN-{n:03}',date='2026-11-08',area=area,severity=severity,status=status,title=title,evidence=evidence,current=current,opportunity=recommendation,impact=f'SEO {seo}/5; rendimiento {perf}/5; UX {ux}/5; mantenibilidad {maint}/5',recommendation=recommendation,alternatives=alternative,dependencies=dependencies,risks=risks,verification=verify,reuse=reuse,scores=dict(benefit=benefit,effort=effort,risk=risk,seo=seo,performance=perf,ux=ux,reusability=shared,maintainability=maint,platform_dependency=platform),priority_score=3*benefit+2*seo+2*perf+2*ux+shared+maint-effort-risk))
add(1,'Arquitectura','Alta','Confirmado','Manifiesto local desactualizado respecto del servidor',
    '[estado remoto](../13-evidence/measurements/source-baseline/remote-themes.json), [diff](../13-evidence/measurements/source-baseline/remote-diff.json), manifest.json L2–4',
    'Local: theme null/versión 1/fork false. Remoto: Ipanema Deco 1.8.0, fork true, publicado; 329 archivos comparables iguales.',
    'Verificar identidad/fork/versión remotos antes de editar; corregir metadatos solo en una operación autorizada. Beneficio: evita elegir un flujo incorrecto sin necesidad de cambiar el tema.',
    'Conservar el manifiesto durante discovery y registrar la contradicción, como se hizo.', 'CLI y lectura autorizada actualizada.', 'Un pull para arreglar metadatos podría sobrescribir cambios locales; no usarlo como reparación automática.', 'Comparar theme list/diff y manifiesto del mismo theme_id.', 'Mismo control para cada tienda; no persistir permisos como un hecho eterno.', (5,1,1,1,1,2,5,5,'alta'))
add(2,'Arquitectura / QA','Alta','Confirmado','La pantalla de password entrega otra instalación',
    '[sin sesión](../13-evidence/measurements/http/owner-public-url.json), [con acceso](../13-evidence/measurements/browser/storefront-discovery.json)',
    'Password usó 14517784/1.2.1; tras acceso autorizado, la home cargó 1.8.0. El motivo interno no está demostrado.',
    'Separar benchmarks y diagnósticos por URL final, sesión y recursos. La barrera inicial quedó resuelta para el auditor; conservar trazabilidad del contexto.',
    'Usar preview explícita y verificar recursos; no atribuir versión por el parámetro solicitado.', 'Sesión storefront autorizada; no se requiere contraseña en archivos.', 'Optimizar o borrar recursos de una instalación distinta por error.', 'Contrastar finalUrl, body template y URLs de scripts con estado remoto.', 'Procedimiento útil en staging, preview y producción de todas las tiendas.', (5,1,1,2,3,3,5,5,'alta'))
add(3,'Componente / Arquitectura','Media','Confirmado','Existen card, imagen y formulario compartidos',
    '[mapa](../01-architecture/dependency-map.md), [cards](../07-commerce/product-cards.md), [PDP](../07-commerce/product-detail.md)',
    'Listados usan item.tpl; bloques products lo reutilizan; destacado reutiliza galería/formulario de PDP; image.tpl es la entrada común.',
    'Extender configuración o variantes pequeñas de las fuentes existentes. Reduce duplicación y mantiene correcciones comunes; exige comprobar consumidores.',
    'Componer bloques nativos si el cambio no requiere markup nuevo.', 'Inventario, contrato de parámetros y alcance global/instancia.', 'Un cambio global puede alterar varios módulos o romper hooks de negocio.', 'Recorrer consumidores reales y probar modos grid/slide/reduced y PDP/destacado.', 'Compartir contratos/patrones; código entre tiendas solo con permisos y versiones compatibles.', (5,2,2,2,4,3,5,5,'media'))
add(4,'Responsive / UX','Alta','Confirmado','Flechas externas provocan overflow en home intermedia',
    '[estado y rectángulos](../13-evidence/measurements/browser/state-audit.json), [matriz](../10-quality/responsive-results.md)',
    'Home: scrollWidth 778 a viewport 768; en otra muestra 1026 a 1024. Botones/SVG de carrusel quedan fuera del ancho. PDP representativa también desborda.',
    'Ajustar posición/anchura de flechas dentro del componente y revisar módulos relacionados. Beneficio: reflow estable sin recortar el sitio globalmente; coste CSS acotado y QA por cortes.',
    'Controles dentro del contenedor o fuera del slider con espacio reservado.', 'CSS del carrusel, padding y tamaños de SVG.', 'Overflow hidden global puede esconder foco, dropdowns o contenido y enmascarar el origen.', 'Repetir 767/768/769 y 1024, rectángulos y scrollWidth en home/PDP.', 'Patrón de controles adaptable a banners, productos y galerías.', (5,2,2,1,2,5,5,4,'baja'))
add(5,'Accesibilidad / UX','Alta','Confirmado','Menú móvil sin gestión de foco/cierre de teclado suficiente',
    '[prueba de estados](../13-evidence/measurements/browser/state-audit.json), captura state-menu-390.png',
    'Foco permanece en disparador, seis Tabs pasan fuera del panel; Escape no lo cierra tras esperar transiciones. axe señala botón de cierre sin nombre.',
    'Definir y aplicar un patrón de navegación/panel accesible en el componente compartido. Gestionar entrada/retorno de foco y cierre; beneficio de teclado directo, con coste de regresión sobre otros modals.',
    'Patrón de navegación expandible no modal si satisface la interacción; no agregar role dialog por inercia.', 'ModalHandler y modal.tpl, navegación y semántica elegida.', 'Una trampa de foco incorrecta puede impedir salir; modificar handler compartido afecta carrito/quick shop/filtros.', 'Teclado completo, Escape, disparador, foco visible, AT y casos anidados.', 'Solución central cuando los consumidores comparten el mismo contrato.', (5,3,3,1,1,5,5,4,'media'))
add(6,'Accesibilidad','Alta','Confirmado','Incidencias de contraste, nombre accesible y tamaño de objetivo',
    '[axe por tipo/ancho](../10-quality/responsive-results.md), [home](../13-evidence/measurements/browser/storefront-viewport-390.json)',
    'Reglas color-contrast y label-content-name-mismatch en home; target-size y contraste en PDP representativa; resultados por nodo en JSON.',
    'Corregir colores/labels y área de interacción en su fuente o instancia, revisando cada nodo. Beneficio AA/uso táctil; coste menor para colores y mayor si cambia layout.',
    'Ajuste de datos de la instancia cuando no hace falta cambiar el componente.', 'Revisión visual y semántica de cada regla, no solo score.', 'Cambiar color global o aria-label indiscriminadamente puede introducir otro fallo.', 'axe y revisión manual a 390/1440, teclado y contraste de estados.', 'Tokens y componentes comunes permiten corregir varias rutas con un solo cambio.', (5,2,2,1,1,5,5,4,'baja'))
add(7,'SEO / Contenido','Media','Confirmado','Nueve PDP añaden un H1 en la descripción del comerciante',
    '[cobertura](../13-evidence/measurements/coverage-summary.json), [ubicación del H1](../13-evidence/measurements/browser/additional-states.json)',
    '9 de 17 PDP tienen dos H1; en la muestra, el segundo está en user-content con clases/estilos Elementor, no en el nombre nativo.',
    'Normalizar jerarquía del contenido de descripción manteniendo el H1 del producto. Beneficio semántico/editorial; revisar contenido antes de una migración, sin arreglarlo escondiendo H1 con CSS.',
    'Guía editorial y correcciones individuales autorizadas de contenido.', 'Acceso de edición del catálogo en una fase posterior; no se editó.', 'Una sustitución automática de todas las etiquetas puede alterar contenido legítimo.', 'Inspeccionar H1 y sus ancestros de las nueve rutas; revisar títulos de descripción.', 'Regla de contenido reusable, sin cambiar product-form para compensar HTML importado.', (4,2,2,4,1,3,4,4,'media'))
add(8,'SEO / Semántica','Media','Confirmado','El bloque heading configura aspecto, no jerarquía HTML',
    'blocks/heading.tpl L32–40; [análisis SEO](../04-seo/technical-seo.md)',
    'Emite div con richtext raw y clases visuales; el comentario que dice p no describe el marcado. Home muestra H1 de tienda pero títulos visuales sin H2/H3 en la muestra.',
    'Definir un contrato explícito de etiqueta semántica en el componente existente si la tarea requiere secciones editoriales. Beneficio de estructura; necesita fork y migración cuidadosa de presets.',
    'Usar contenido semántico permitido y revisado por editor, comprobando qué marcado conserva.', 'Jerarquía por página, richtext y reglas del editor.', 'Convertir todos los títulos a H1 o derivar tag del tamaño visual genera una jerarquía incorrecta.', 'Comparar outline del HTML inicial y del renderizado por tipo de página.', 'Separar tamaño visual de semántica es un patrón portable.', (4,3,3,4,1,3,5,4,'media'))
add(9,'SEO / Catálogo','Alta','Confirmado','La paginación infinite activa carece de enlace siguiente en su control',
    'category.json; pagination.tpl L10–23; [sin JS](../13-evidence/measurements/browser/no-js-commerce.json)',
    'Categoría guarda infinite. El anchor Mostrar más tiene href null; sin JS conserva 12 productos iniciales y no ofrece ese enlace siguiente.',
    'Conservar URL real de página siguiente en un enhancement o usar paginación clásica nativa. Mejora rastreo/fallback sin otro motor; revisar cursores, filtros y UX.',
    'Grid/paginación clásica configurables sin reescribir LS.', 'URLs/cursor de plataforma y decisión UX sobre carga incremental.', 'Construir ?page= por suposición puede romper variantes como productos y estado de filtros.', 'Sin JS, seguir enlaces a páginas posteriores; con JS comprobar historial, productos y reintentos.', 'Aplicable a categorías/búsqueda de cada tienda con ese modo.', (5,3,3,5,2,4,5,4,'media'))
add(10,'Rendimiento / Resiliencia','Media','Confirmado','Sin JS quedan imágenes transparentes y CSS async en print',
    '[sin JS comercio](../13-evidence/measurements/browser/no-js-commerce.json), layout.tpl L29, image.tpl',
    'En la muestra categoría hay 12 imágenes con opacity 0 y en PDP 13; el link async permanece media print. No todas son imágenes visibles del primer viewport.',
    'Mejorar progresivamente el helper y estrategia CSS: contenido/medios esenciales visibles si falla JS, sin duplicar página. Beneficio resiliencia; coste revisar callers y prioridades.',
    'Lazy nativo y fallback acotado donde lo soporte la plataforma.', 'Cascada, src/srcset y motores lazy existentes.', 'Cargar todas las imágenes eagerly para arreglar fallback puede empeorar LCP/red.', 'Desactivar JS, revisar imagen principal, navegación, estado final y recursos.', 'Una corrección común puede beneficiar todos los componentes que usan image.tpl.', (4,3,3,3,3,4,5,4,'media'))
add(11,'Rendimiento / LCP','Alta','Confirmado','El hero placeholder se convierte en LCP y usa lazy JS',
    '[Lighthouse home mobile](../13-evidence/measurements/lighthouse/home-mobile.json), hero.tpl L66–77',
    'El candidato LCP fue el img placeholder del hero. LCP simulado mobile 4.133 s; el source de esa rama usa fade-in/lazy JS.',
    'Definir el medio final y medir la prioridad de esa misma rama; si el placeholder permanece visible, no diferir el LCP por JS. Beneficio de carga inicial; no prometer ahorro exacto ni optimizar solo datos de ejemplo.',
    'Hero estático con un medio responsive y texto inicial, usando helper existente.', 'Contenido de marca, posición real del hero y perfil de red.', 'Precargar todas las secciones o sacrificar calidad de producto puede mover el cuello de botella.', 'Mismo hero final, caché fría, candidato LCP y waterfall antes/después.', 'Criterio de primera imagen configurable en otras tiendas.', (5,2,2,2,5,4,5,4,'media'))
add(12,'Rendimiento / JavaScript','Alta','Confirmado','Las tres muestras móviles muestran bloqueo sustancial',
    '[resultados Lighthouse](../05-performance/storefront-lighthouse-results.md)',
    'TBT mobile: home 403 ms, categoría 417 ms, PDP 485 ms. No es INP ni dato de usuarios reales.',
    'Perfilar tareas y dependencias de cada ruta antes de reducir código; evitar nuevos motores/listeners y evaluar carga por feature. Beneficio de capacidad de respuesta; coste de perfilado y compatibilidad LS.',
    'Desactivar por settings lo que no se usa, midiendo función y efecto.', 'Traza, scripts de plataforma/tema separados y escenarios de interacción.', 'Borrar unused JS de una sola navegación puede romper variantes y carrito después.', 'Traza con CPU móvil y acciones representativas; repetir si hay variación.', 'Presupuesto incremental y arquitectura común para todas las tiendas.', (5,4,4,2,5,4,5,5,'alta'))
add(13,'Rendimiento / Imágenes','Media','Confirmado + impacto estimado','sizes de cards y medios sobredimensionados merecen ajuste',
    'item-image.tpl L87–100; [Lighthouse PDP](../13-evidence/measurements/lighthouse/pdp-mobile.json)',
    'Card declara 50vw desktop aun con cuatro columnas. Lighthouse estima oportunidades de entrega de imágenes, hasta ~95 KiB en la muestra PDP; no es ahorro obtenido.',
    'Pasar sizes según contenedor/columnas al helper y revisar imagen/logotipo entregados con DPR real. Beneficio de red/decodificación; coste medir y conservar calidad.',
    'Reconfigurar archivos de medios adecuados antes de tocar lógica cuando el origen es el asset.', 'Ancho renderizado, srcset, currentSrc y Network.', 'Confundir naturalWidth con píxeles crudos o reducir de más en retina.', 'Comparar selección y bytes a DPR 1/2 y varios anchos, con calidad visual.', 'Extensión parametrizada del helper compartido, sin otra implementación.', (4,3,3,2,4,3,5,4,'media'))
add(14,'Rendimiento / Responsive','Media','Inferido','Dos elementos de imagen responsive pueden competir por red',
    'hero.tpl L50–95; blocks/slide.tpl L49–103; [análisis](../05-performance/image-loading.md)',
    'Las ramas de arte desktop/mobile son imgs separados y mobile puede ser high priority oculto en desktop. No se configuraron ambas variantes para forzar una prueba durante discovery.',
    'Evaluar art direction con un picture compartido y sources media en el helper existente. Beneficio potencial de red; requiere comprobar capacidades de medios y todos los callers.',
    'Conservar estrategia actual si Network demuestra que solo carga el recurso útil en el caso real.', 'Medios desktop/mobile reales y prueba de red por componente.', 'Cambiar lazy o perder selección de formato puede empeorar LCP o dejar imágenes vacías al resize.', 'Distinguir solicitado/completado/decodificado/renderizado/visible; no inferir descarga desde DOM.', 'Patrón general, todavía no una mejora cuantificada de esta configuración.', (4,4,4,1,4,3,5,4,'media'))
add(15,'Arquitectura / Accesibilidad','Media','Confirmado','IDs repetidos en bloques y formularios del DOM',
    '[inventario de duplicados](../13-evidence/measurements/browser/state-audit.json)',
    'Home: 14 grupos de IDs repetidos, incluidos ns-block-heading y variation_1; categoría/PDP también repiten variation_1. Hay clones de slider, pero no todo duplicado se atribuye a ellos.',
    'Trazar la fuente de cada ID y sus consumidores antes de generar identificadores por instancia. Beneficio potencial para labels/selectores; se debe demostrar qué relaciones se afectan.',
    'Usar scopes de componente al buscar nodos cuando el contrato existente lo permita.', 'block_attributes de plataforma, inputs y motor de slider.', 'Renombrar IDs sin actualizar for/ARIA/editor rompe relaciones; no hay prueba de fallo de cada duplicado.', 'Cruzar id/for/aria-controls y búsqueda JS con card repetida y clones.', 'Regla de identidad por instancia para componentes compartidos.', (4,3,4,1,1,4,5,5,'alta'))
add(16,'CSS / Mantenibilidad','Media','Confirmado','La capa nativa de utilidades explica gran parte de !important',
    '[medidas CSS](../05-performance/static-asset-measurements.md), [cascada](../03-editor/responsive-controls.md)',
    'CSS critical/utilities/async: 15/496/23 ocurrencias; también hay estilos inline por settings.',
    'Modificar control/fuente responsable y acotar variantes antes de un override. Beneficio de mantenibilidad; no borrar utilidades nativas para bajar un contador.',
    'Excepción !important justificada y documentada cuando el contrato externo la exige.', 'Estilo computado, origen de regla y alcance real.', 'Cambiar CSS global o moverlo a layers sin entender prioridad puede extender regresiones.', 'Inspeccionar cascada en los nodos afectados y comparar dispositivos.', 'Política compartida de estilo limpio, con branding por tienda.', (4,2,2,1,2,3,5,5,'baja'))
add(17,'SEO / Datos estructurados','Media','Confirmado','JSON-LD WebPage inválido en la ruta 404',
    '[rutas y parseo](../10-quality/runtime-page-audit.md), structured-data.tpl L175–221',
    'La sonda devuelve HTTP 404 correctamente, pero el objeto WebPage falla al parsear. El patrón de coma previa y breadcrumbs vacíos también se observó en password.',
    'Serializar la lista sin coma dependiente de que haya breadcrumbs. Beneficio de consistencia sintáctica; revisar todas las ramas del snippet existente.',
    'Omitir elementos inexistentes de forma válida, manteniendo Organization y el contenido permitido.', 'Twig/JSON-LD compartido y casos de lista vacía.', 'Agregar otro JSON-LD no corrige el bloque inválido y puede duplicar entidades.', 'JSON.parse de todos los scripts en 404, home, PDP, blog, búsqueda y páginas sin breadcrumbs.', 'Patrón de serialización aplicable a cualquier plantilla.', (4,2,2,4,1,2,5,4,'media'))
add(18,'SEO / Accesibilidad','Media','Confirmado','La 404 observada tiene title vacío',
    '[matriz responsive](../10-quality/responsive-results.md), axe document-title de 404',
    'HTTP 404 y H1 existen, pero document.title está vacío; password inicial comparte esa carencia en otro contexto.',
    'Revisar metadatos de plataforma para esa ruta y definir título útil por el mecanismo soportado. Beneficio para orientación/AT; no insertar otro title global.',
    'Escalar a soporte de plataforma si head-tags no ofrece control para ese caso.', 'Componente privado head-tags y configuración disponible.', 'Una solución Twig global podría duplicar metadatos en todas las otras páginas.', 'HTML inicial contiene un único title útil en la 404 sin afectar otras rutas.', 'Criterio de QA reusable; solución depende de plataforma.', (3,2,3,2,1,3,4,4,'alta'))
add(19,'SEO / Reutilización','Baja','Confirmado','El tema ya emite JSON-LD de organización, página y producto',
    '[tipos y condiciones](../04-seo/structured-data.md), HTML inicial del crawl',
    'Organization global, WebPage/BreadcrumbList, Product/Offer por contexto y Blog/BlogPosting ya están presentes.',
    'Auditar coherencia antes de agregar plugins o schema manual. Beneficio de evitar señales duplicadas sin bytes nuevos; requiere revisar apps instaladas, todavía no auditadas en Admin.',
    'Agregar únicamente un tipo pertinente ausente, con datos verificables y semántica definida.', 'Estado de apps y requisitos vigentes del buscador.', 'Inventar reseñas/ratings/precio o prometer rich results no respaldados.', 'Comparar entidades por URL/ID y valores visibles; validadores separados de JSON.parse.', 'Playbook común que evita repetir desarrollo SEO innecesario.', (4,1,1,4,2,2,5,5,'media'))
add(20,'SEO / Lanzamiento','Media','Confirmado en el contexto probado','La protección de tienda cambia el acceso del rastreador',
    '[sin sesión](../13-evidence/measurements/http/route-probes.json), [robots con sesión](../13-evidence/measurements/crawl/robots.txt)',
    'Sin sesión hubo password; con sesión, robots/sitemap accesibles. Robots declara restricciones de cuenta, búsqueda, carrito y preview. CDN gzip rechazó al cliente HTTP de auditoría con 403.',
    'Antes del lanzamiento repetir endpoints sin sesión y verificar acceso de buscadores, manteniendo la protección hasta que el propietario decida publicar. No tratar el estado intencional de password como una avería.',
    'Validación de lanzamiento en una ventana autorizada y Search Console del propietario.', 'Decisión comercial y control de plataforma.', 'Quitar contraseña para probar expone la tienda; un 403 de esta herramienta no prueba bloqueo de Googlebot.', 'GET sin cookies, respuesta final y sitemap/robots reales al lanzar.', 'Puerta de verificación para todas las tiendas, sin cambios durante discovery.', (4,1,2,5,1,2,5,4,'alta'))
add(21,'Motion / Accesibilidad','Media','Confirmado en source; variantes no comprobadas','Reduced-motion no cubre todas las animaciones opcionales',
    '[motion nativo](../06-motion/native-animations.md), critical.css L328/L355 y store.js L3958',
    'Hay protección de hero/slideshow/utilidades y parallax, pero no se comprobó una política integral para marquee/loaders/autoplay.',
    'Revisar cada efecto activado y ofrecer alternativa estática/pausa cuando corresponda. Beneficio de lectura/control; coste bajo de CSS y mayor si requiere cambiar motor.',
    'No activar efectos sin valor UX demostrado.', 'Settings reales y comportamiento de los motores existentes.', 'Deshabilitar todo sin considerar feedback de carga o estado puede quitar información.', 'Reduce al cargar/cambiar preferencia, foco, teclado y autoplay con datos reales.', 'Tokens/política de motion compartidos, efectos concretos por tienda.', (4,2,2,1,2,4,5,4,'media'))
add(22,'Reutilización / Licencias','Media','No comprobado: permiso de redistribución','No hay licencia de tema encontrada que autorice una biblioteca entre tiendas',
    '[inventario](../01-architecture/directory-map.md), [multitienda](../08-design-system/multi-store-strategy.md)',
    'Se tiene autorización de inspección de este proyecto; no se encontró licencia del tema en su raíz ni permiso de transferencia de implementación.',
    'Compartir metodología/contratos y código propio con procedencia registrada; verificar derechos antes de distribuir archivos del tema. Beneficio de sostenibilidad; limita la copia directa, no la investigación.',
    'App propia con interfaces oficiales o patrones implementados de forma independiente.', 'Permisos/licencias del titular, assets y terceros por separado.', 'La licencia de Craft Anything no se extiende a Ipanema o marcas del comerciante.', 'Registrar fuente y permiso de cada unidad que se quiera distribuir.', 'Arquitectura de conocimiento portable sin confundirla con licencia de código.', (4,1,2,1,1,2,5,5,'alta'))
add(23,'Editor / Configuración','Media','Confirmado','Los valores efectivos pueden ser de sección y no globales',
    'settings_data.json pagination classic; templates/pages/category.json pagination infinite; [matriz](../02-native-components/settings-matrix.md)',
    'El mismo concepto existe en capas distintas; cambiar un setting global no garantiza modificar una sección que guarda su propio valor.',
    'Registrar fuente efectiva, default de schema y fallback Twig antes de tocar CSS. Beneficio de cambios más pequeños y reversibles; coste de rastrear la instancia.',
    'Configurar la instancia desde editor cuando el control existe, sin cambiar código.', 'Schema del padre/bloque y datos guardados actuales.', 'Sobrescribir datos para uniformar una tienda puede borrar decisiones del comerciante.', 'Seguir valor guardado → Twig → clases/estilos computados.', 'Método determinista de personalización para todas las tiendas.', (4,1,1,2,2,3,5,5,'media'))
add(24,'Responsive / JavaScript','Media','Inferido','Inicialización por ancho merece comprobarse tras resize',
    'store.js L175–186, L318–324, L368–371; [galerías](../07-commerce/carousels-and-galleries.md)',
    'Varias ramas hacen return según innerWidth al inicializar. La matriz prueba cargas independientes; no demuestra reconstrucción correcta al cruzar todos los cortes.',
    'Probar orientación/resize y definir destroy/reinit solo donde falle el contrato existente. Beneficio de consistencia; evita dos copias del contenido, pero exige cleanup.',
    'CSS responsive con scroll nativo si cubre el caso sin estado de motor.', 'Instancias Swiper, listeners y datos de configuración.', 'Reinicializar indiscriminadamente puede duplicar sliders o perder posición/foco.', 'Secuencia 390→768→390 y 1024→767, inspeccionando instancia, visibilidad y recursos.', 'Contrato de ciclo de vida para módulos reutilizables.', (3,3,3,1,2,3,5,4,'baja'))

def main():
    problems={
      1:'La capa local de metadatos puede conducir a una decisión de permisos o versión incorrecta.',
      2:'Medir una superficie distinta puede producir un diagnóstico y una intervención equivocados.',
      3:'Duplicar esas unidades desperdiciaría lógica existente y multiplicaría mantenimiento.',
      4:'El ancho visible excede el viewport en cortes intermedios y afecta reflow.',
      5:'El recorrido de teclado no acompaña al panel visual abierto.',
      6:'La experiencia necesita correcciones por nodo; el score global no identifica por sí solo su solución.',
      7:'El contenido importado altera la jerarquía de la PDP sin que el formulario nativo sea el origen.',
      8:'La configuración de tamaño visual no garantiza encabezados que describan las secciones.',
      9:'El control de carga no conserva una vía de navegación HTML a productos posteriores.',
      10:'La presentación de parte de los medios depende de que se ejecute el enhancement.',
      11:'La estrategia de carga actual difiere un medio que termina siendo el mayor contenido visual.',
      12:'El trabajo de carga móvil merece perfilado antes de sumar funciones o dependencias.',
      13:'La selección del recurso puede exceder el tamaño necesario para la tarjeta o medio.',
      14:'La arquitectura de dos img plantea una hipótesis de descarga que aún exige una configuración real para comprobarla.',
      15:'Las relaciones por ID necesitan revisión, separando duplicación estática, formularios y clones.',
      16:'Los parches pueden escalar especificidad si se ignoran inline y utilidades del tema.',
      17:'Una lista vacía deja un objeto de datos estructurados sintácticamente inválido.',
      18:'La página de error carece de un título documental útil.',
      19:'Añadir otro generador sin inventario puede duplicar entidades y valores.',
      20:'Las pruebas con sesión no acreditan cómo podrá rastrear la tienda un visitante sin acceso.',
      21:'No se dispone de evidencia de cobertura integral de motion accesible en todos los efectos.',
      22:'La autorización de inspección no resuelve el permiso de distribución entre comerciantes.',
      23:'Un ajuste en la capa equivocada puede no producir el cambio o borrar una elección de instancia.',
      24:'Un layout correcto tras recarga puede tener estado interactivo incorrecto después de cruzar un corte.'}
    for f in F:
        f['opportunity']=problems[int(f['id'].split('-')[1])]
        if f['status'].startswith('Confirmado'):f['status']='Confirmado'
        elif f['status'].startswith('No comprobado'):f['status']='No comprobado'
    out=R/'11-opportunities';out.mkdir(parents=True,exist_ok=True)
    (out/'findings.json').write_text(json.dumps(F,ensure_ascii=False,indent=2)+'\n')
    text=['# Hallazgos técnicos y oportunidades', '', 'Verificado 2026-11-08. Estado y severidad corresponden a la evidencia indicada; ninguna solución se implementó en el tema. No hay una vulnerabilidad crítica demostrada por esta auditoría. Los resultados de password y storefront están separados.', '']
    fields=[('Área','area'),('Hallazgo','title'),('Evidencia','evidence'),('Estado','status'),('Comportamiento actual','current'),('Problema u oportunidad','opportunity'),('Impacto','impact'),('Severidad','severity'),('Solución recomendada','recommendation'),('Alternativas','alternatives'),('Dependencias','dependencies'),('Riesgos','risks'),('Cómo verificar','verification'),('Reutilización','reuse')]
    for f in F:
        text.extend([f'## {f["id"]}', '', f'**Identificador:** {f["id"]} · **Fecha:** {f["date"]}', ''])
        text.extend(f'**{label}:** {f[key]}\n' for label,key in fields)
    (out/'critical-findings.md').write_text('\n'.join(text)+'\n')
    rows=['# Matriz de prioridad', '', 'Escalas estimadas de 1 (menor) a 5 (mayor), basadas en exposición comprobada, impacto funcional, alcance de consumidores y complejidad. Son juicio de ingeniería explícito, no ROI medido. Severidad no depende de facilidad. Esfuerzo y riesgo altos reducen la prioridad de una intervención inmediata, no su importancia.', '', 'Puntaje = 3×beneficio + 2×SEO + 2×rendimiento + 2×UX + reutilización + mantenibilidad − esfuerzo − riesgo. Dependencia de plataforma se registra aparte; algunos cambios necesitan datos/permisos antes de poder implementarse.', '', '| ID | Beneficio | Esfuerzo | Riesgo | SEO | Rend. | UX | Reúso | Mant. | Plataforma | Puntaje |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|']
    for f in sorted(F,key=lambda x:-x['priority_score']):
        s=f['scores'];vals=[f'[{f["id"]}](critical-findings.md#{f["id"].lower()})',*[str(s[k]) for k in ['benefit','effort','risk','seo','performance','ux','reusability','maintainability','platform_dependency']],str(f['priority_score'])];rows.append('| '+' | '.join(vals)+' |')
    (out/'priority-matrix.md').write_text('\n'.join(rows)+'\n')
    print(json.dumps({'findings':len(F),'confirmed':sum(f['status'].startswith('Confirmado') for f in F),'inferred':sum(f['status']=='Inferido' for f in F)},ensure_ascii=False))
if __name__=='__main__':main()
