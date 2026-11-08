# Hallazgos técnicos y oportunidades

Verificado 2026-11-08. Estado y severidad corresponden a la evidencia indicada; ninguna solución se implementó en el tema. No hay una vulnerabilidad crítica demostrada por esta auditoría. Los resultados de password y storefront están separados.

Revalidación SEO V2.1: [auditoría viva y hallazgos SEO-IPN](../../reports/seo/audited-pages.md) confirma nuevamente la coma JSON-LD de 404, el H1 editorial adicional y el control de carga de catálogo sin href. Distingue defectos de falsos positivos del QA corregidos y conserva los estados originales; no convierte la propuesta de parche en solución desplegada. [Motor de validación](../04-seo/seo-engine.md).

## IPN-001

**Identificador:** IPN-001 · **Fecha:** 2026-11-08

**Área:** Arquitectura

**Hallazgo:** Manifiesto local desactualizado respecto del servidor

**Evidencia:** [estado remoto](../13-evidence/measurements/source-baseline/remote-themes.json), [diff](../13-evidence/measurements/source-baseline/remote-diff.json), manifest.json L2–4

**Estado:** Confirmado

**Comportamiento actual:** Local: theme null/versión 1/fork false. Remoto: Ipanema Deco 1.8.0, fork true, publicado; 329 archivos comparables iguales.

**Problema u oportunidad:** La capa local de metadatos puede conducir a una decisión de permisos o versión incorrecta.

**Impacto:** SEO 1/5; rendimiento 1/5; UX 2/5; mantenibilidad 5/5

**Severidad:** Alta

**Solución recomendada:** Verificar identidad/fork/versión remotos antes de editar; corregir metadatos solo en una operación autorizada. Beneficio: evita elegir un flujo incorrecto sin necesidad de cambiar el tema.

**Alternativas:** Conservar el manifiesto durante discovery y registrar la contradicción, como se hizo.

**Dependencias:** CLI y lectura autorizada actualizada.

**Riesgos:** Un pull para arreglar metadatos podría sobrescribir cambios locales; no usarlo como reparación automática.

**Cómo verificar:** Comparar theme list/diff y manifiesto del mismo theme_id.

**Reutilización:** Mismo control para cada tienda; no persistir permisos como un hecho eterno.

## IPN-002

**Identificador:** IPN-002 · **Fecha:** 2026-11-08

**Área:** Arquitectura / QA

**Hallazgo:** La pantalla de password entrega otra instalación

**Evidencia:** [sin sesión](../13-evidence/measurements/http/owner-public-url.json), [con acceso](../13-evidence/measurements/browser/storefront-discovery.json)

**Estado:** Confirmado

**Comportamiento actual:** Password usó 14517784/1.2.1; tras acceso autorizado, la home cargó 1.8.0. El motivo interno no está demostrado.

**Problema u oportunidad:** Medir una superficie distinta puede producir un diagnóstico y una intervención equivocados.

**Impacto:** SEO 2/5; rendimiento 3/5; UX 3/5; mantenibilidad 5/5

**Severidad:** Alta

**Solución recomendada:** Separar benchmarks y diagnósticos por URL final, sesión y recursos. La barrera inicial quedó resuelta para el auditor; conservar trazabilidad del contexto.

**Alternativas:** Usar preview explícita y verificar recursos; no atribuir versión por el parámetro solicitado.

**Dependencias:** Sesión storefront autorizada; no se requiere contraseña en archivos.

**Riesgos:** Optimizar o borrar recursos de una instalación distinta por error.

**Cómo verificar:** Contrastar finalUrl, body template y URLs de scripts con estado remoto.

**Reutilización:** Procedimiento útil en staging, preview y producción de todas las tiendas.

## IPN-003

**Identificador:** IPN-003 · **Fecha:** 2026-11-08

**Área:** Componente / Arquitectura

**Hallazgo:** Existen card, imagen y formulario compartidos

**Evidencia:** [mapa](../01-architecture/dependency-map.md), [cards](../07-commerce/product-cards.md), [PDP](../07-commerce/product-detail.md)

**Estado:** Confirmado

**Comportamiento actual:** Listados usan item.tpl; bloques products lo reutilizan; destacado reutiliza galería/formulario de PDP; image.tpl es la entrada común.

**Problema u oportunidad:** Duplicar esas unidades desperdiciaría lógica existente y multiplicaría mantenimiento.

**Impacto:** SEO 2/5; rendimiento 4/5; UX 3/5; mantenibilidad 5/5

**Severidad:** Media

**Solución recomendada:** Extender configuración o variantes pequeñas de las fuentes existentes. Reduce duplicación y mantiene correcciones comunes; exige comprobar consumidores.

**Alternativas:** Componer bloques nativos si el cambio no requiere markup nuevo.

**Dependencias:** Inventario, contrato de parámetros y alcance global/instancia.

**Riesgos:** Un cambio global puede alterar varios módulos o romper hooks de negocio.

**Cómo verificar:** Recorrer consumidores reales y probar modos grid/slide/reduced y PDP/destacado.

**Reutilización:** Compartir contratos/patrones; código entre tiendas solo con permisos y versiones compatibles.

## IPN-004

**Identificador:** IPN-004 · **Fecha:** 2026-11-08

**Área:** Responsive / UX

**Hallazgo:** Flechas externas provocan overflow en home intermedia

**Evidencia:** [estado y rectángulos](../13-evidence/measurements/browser/state-audit.json), [matriz](../10-quality/responsive-results.md)

**Estado:** Confirmado

**Comportamiento actual:** Home: scrollWidth 778 a viewport 768; en otra muestra 1026 a 1024. Botones/SVG de carrusel quedan fuera del ancho. PDP representativa también desborda.

**Problema u oportunidad:** El ancho visible excede el viewport en cortes intermedios y afecta reflow.

**Impacto:** SEO 1/5; rendimiento 2/5; UX 5/5; mantenibilidad 4/5

**Severidad:** Alta

**Solución recomendada:** Ajustar posición/anchura de flechas dentro del componente y revisar módulos relacionados. Beneficio: reflow estable sin recortar el sitio globalmente; coste CSS acotado y QA por cortes.

**Alternativas:** Controles dentro del contenedor o fuera del slider con espacio reservado.

**Dependencias:** CSS del carrusel, padding y tamaños de SVG.

**Riesgos:** Overflow hidden global puede esconder foco, dropdowns o contenido y enmascarar el origen.

**Cómo verificar:** Repetir 767/768/769 y 1024, rectángulos y scrollWidth en home/PDP.

**Reutilización:** Patrón de controles adaptable a banners, productos y galerías.

## IPN-005

**Identificador:** IPN-005 · **Fecha:** 2026-11-08

**Área:** Accesibilidad / UX

**Hallazgo:** Menú móvil sin gestión de foco/cierre de teclado suficiente

**Evidencia:** [prueba de estados](../13-evidence/measurements/browser/state-audit.json), captura state-menu-390.png

**Estado:** Confirmado

**Comportamiento actual:** Foco permanece en disparador, seis Tabs pasan fuera del panel; Escape no lo cierra tras esperar transiciones. axe señala botón de cierre sin nombre.

**Problema u oportunidad:** El recorrido de teclado no acompaña al panel visual abierto.

**Impacto:** SEO 1/5; rendimiento 1/5; UX 5/5; mantenibilidad 4/5

**Severidad:** Alta

**Solución recomendada:** Definir y aplicar un patrón de navegación/panel accesible en el componente compartido. Gestionar entrada/retorno de foco y cierre; beneficio de teclado directo, con coste de regresión sobre otros modals.

**Alternativas:** Patrón de navegación expandible no modal si satisface la interacción; no agregar role dialog por inercia.

**Dependencias:** ModalHandler y modal.tpl, navegación y semántica elegida.

**Riesgos:** Una trampa de foco incorrecta puede impedir salir; modificar handler compartido afecta carrito/quick shop/filtros.

**Cómo verificar:** Teclado completo, Escape, disparador, foco visible, AT y casos anidados.

**Reutilización:** Solución central cuando los consumidores comparten el mismo contrato.

## IPN-006

**Identificador:** IPN-006 · **Fecha:** 2026-11-08

**Área:** Accesibilidad

**Hallazgo:** Incidencias de contraste, nombre accesible y tamaño de objetivo

**Evidencia:** [axe por tipo/ancho](../10-quality/responsive-results.md), [home](../13-evidence/measurements/browser/storefront-viewport-390.json)

**Estado:** Confirmado

**Comportamiento actual:** Reglas color-contrast y label-content-name-mismatch en home; target-size y contraste en PDP representativa; resultados por nodo en JSON.

**Problema u oportunidad:** La experiencia necesita correcciones por nodo; el score global no identifica por sí solo su solución.

**Impacto:** SEO 1/5; rendimiento 1/5; UX 5/5; mantenibilidad 4/5

**Severidad:** Alta

**Solución recomendada:** Corregir colores/labels y área de interacción en su fuente o instancia, revisando cada nodo. Beneficio AA/uso táctil; coste menor para colores y mayor si cambia layout.

**Alternativas:** Ajuste de datos de la instancia cuando no hace falta cambiar el componente.

**Dependencias:** Revisión visual y semántica de cada regla, no solo score.

**Riesgos:** Cambiar color global o aria-label indiscriminadamente puede introducir otro fallo.

**Cómo verificar:** axe y revisión manual a 390/1440, teclado y contraste de estados.

**Reutilización:** Tokens y componentes comunes permiten corregir varias rutas con un solo cambio.

## IPN-007

**Identificador:** IPN-007 · **Fecha:** 2026-11-08

**Área:** SEO / Contenido

**Hallazgo:** Nueve PDP añaden un H1 en la descripción del comerciante

**Evidencia:** [cobertura](../13-evidence/measurements/coverage-summary.json), [ubicación del H1](../13-evidence/measurements/browser/additional-states.json)

**Estado:** Confirmado

**Comportamiento actual:** 9 de 17 PDP tienen dos H1; en la muestra, el segundo está en user-content con clases/estilos Elementor, no en el nombre nativo.

**Problema u oportunidad:** El contenido importado altera la jerarquía de la PDP sin que el formulario nativo sea el origen.

**Impacto:** SEO 4/5; rendimiento 1/5; UX 3/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Normalizar jerarquía del contenido de descripción manteniendo el H1 del producto. Beneficio semántico/editorial; revisar contenido antes de una migración, sin arreglarlo escondiendo H1 con CSS.

**Alternativas:** Guía editorial y correcciones individuales autorizadas de contenido.

**Dependencias:** Acceso de edición del catálogo en una fase posterior; no se editó.

**Riesgos:** Una sustitución automática de todas las etiquetas puede alterar contenido legítimo.

**Cómo verificar:** Inspeccionar H1 y sus ancestros de las nueve rutas; revisar títulos de descripción.

**Reutilización:** Regla de contenido reusable, sin cambiar product-form para compensar HTML importado.

## IPN-008

**Identificador:** IPN-008 · **Fecha:** 2026-11-08

**Área:** SEO / Semántica

**Hallazgo:** El bloque heading configura aspecto, no jerarquía HTML

**Evidencia:** blocks/heading.tpl L32–40; [análisis SEO](../04-seo/technical-seo.md)

**Estado:** Confirmado

**Comportamiento actual:** Emite div con richtext raw y clases visuales; el comentario que dice p no describe el marcado. Home muestra H1 de tienda pero títulos visuales sin H2/H3 en la muestra.

**Problema u oportunidad:** La configuración de tamaño visual no garantiza encabezados que describan las secciones.

**Impacto:** SEO 4/5; rendimiento 1/5; UX 3/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Definir un contrato explícito de etiqueta semántica en el componente existente si la tarea requiere secciones editoriales. Beneficio de estructura; necesita fork y migración cuidadosa de presets.

**Alternativas:** Usar contenido semántico permitido y revisado por editor, comprobando qué marcado conserva.

**Dependencias:** Jerarquía por página, richtext y reglas del editor.

**Riesgos:** Convertir todos los títulos a H1 o derivar tag del tamaño visual genera una jerarquía incorrecta.

**Cómo verificar:** Comparar outline del HTML inicial y del renderizado por tipo de página.

**Reutilización:** Separar tamaño visual de semántica es un patrón portable.

## IPN-009

**Identificador:** IPN-009 · **Fecha:** 2026-11-08

**Área:** SEO / Catálogo

**Hallazgo:** La paginación infinite activa carece de enlace siguiente en su control

**Evidencia:** category.json; pagination.tpl L10–23; [sin JS](../13-evidence/measurements/browser/no-js-commerce.json)

**Estado:** Confirmado

**Comportamiento actual:** Categoría guarda infinite. El anchor Mostrar más tiene href null; sin JS conserva 12 productos iniciales y no ofrece ese enlace siguiente.

**Problema u oportunidad:** El control de carga no conserva una vía de navegación HTML a productos posteriores.

**Impacto:** SEO 5/5; rendimiento 2/5; UX 4/5; mantenibilidad 4/5

**Severidad:** Alta

**Solución recomendada:** Conservar URL real de página siguiente en un enhancement o usar paginación clásica nativa. Mejora rastreo/fallback sin otro motor; revisar cursores, filtros y UX.

**Alternativas:** Grid/paginación clásica configurables sin reescribir LS.

**Dependencias:** URLs/cursor de plataforma y decisión UX sobre carga incremental.

**Riesgos:** Construir ?page= por suposición puede romper variantes como productos y estado de filtros.

**Cómo verificar:** Sin JS, seguir enlaces a páginas posteriores; con JS comprobar historial, productos y reintentos.

**Reutilización:** Aplicable a categorías/búsqueda de cada tienda con ese modo.

## IPN-010

**Identificador:** IPN-010 · **Fecha:** 2026-11-08

**Área:** Rendimiento / Resiliencia

**Hallazgo:** Sin JS quedan imágenes transparentes y CSS async en print

**Evidencia:** [sin JS comercio](../13-evidence/measurements/browser/no-js-commerce.json), layout.tpl L29, image.tpl

**Estado:** Confirmado

**Comportamiento actual:** En la muestra categoría hay 12 imágenes con opacity 0 y en PDP 13; el link async permanece media print. No todas son imágenes visibles del primer viewport.

**Problema u oportunidad:** La presentación de parte de los medios depende de que se ejecute el enhancement.

**Impacto:** SEO 3/5; rendimiento 3/5; UX 4/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Mejorar progresivamente el helper y estrategia CSS: contenido/medios esenciales visibles si falla JS, sin duplicar página. Beneficio resiliencia; coste revisar callers y prioridades.

**Alternativas:** Lazy nativo y fallback acotado donde lo soporte la plataforma.

**Dependencias:** Cascada, src/srcset y motores lazy existentes.

**Riesgos:** Cargar todas las imágenes eagerly para arreglar fallback puede empeorar LCP/red.

**Cómo verificar:** Desactivar JS, revisar imagen principal, navegación, estado final y recursos.

**Reutilización:** Una corrección común puede beneficiar todos los componentes que usan image.tpl.

## IPN-011

**Identificador:** IPN-011 · **Fecha:** 2026-11-08

**Área:** Rendimiento / LCP

**Hallazgo:** El hero placeholder se convierte en LCP y usa lazy JS

**Evidencia:** [Lighthouse home mobile](../13-evidence/measurements/lighthouse/home-mobile.json), hero.tpl L66–77

**Estado:** Confirmado

**Comportamiento actual:** El candidato LCP fue el img placeholder del hero. LCP simulado mobile 4.133 s; el source de esa rama usa fade-in/lazy JS.

**Problema u oportunidad:** La estrategia de carga actual difiere un medio que termina siendo el mayor contenido visual.

**Impacto:** SEO 2/5; rendimiento 5/5; UX 4/5; mantenibilidad 4/5

**Severidad:** Alta

**Solución recomendada:** Definir el medio final y medir la prioridad de esa misma rama; si el placeholder permanece visible, no diferir el LCP por JS. Beneficio de carga inicial; no prometer ahorro exacto ni optimizar solo datos de ejemplo.

**Alternativas:** Hero estático con un medio responsive y texto inicial, usando helper existente.

**Dependencias:** Contenido de marca, posición real del hero y perfil de red.

**Riesgos:** Precargar todas las secciones o sacrificar calidad de producto puede mover el cuello de botella.

**Cómo verificar:** Mismo hero final, caché fría, candidato LCP y waterfall antes/después.

**Reutilización:** Criterio de primera imagen configurable en otras tiendas.

## IPN-012

**Identificador:** IPN-012 · **Fecha:** 2026-11-08

**Área:** Rendimiento / JavaScript

**Hallazgo:** Las tres muestras móviles muestran bloqueo sustancial

**Evidencia:** [resultados Lighthouse](../05-performance/storefront-lighthouse-results.md)

**Estado:** Confirmado

**Comportamiento actual:** TBT mobile: home 403 ms, categoría 417 ms, PDP 485 ms. No es INP ni dato de usuarios reales.

**Problema u oportunidad:** El trabajo de carga móvil merece perfilado antes de sumar funciones o dependencias.

**Impacto:** SEO 2/5; rendimiento 5/5; UX 4/5; mantenibilidad 5/5

**Severidad:** Alta

**Solución recomendada:** Perfilar tareas y dependencias de cada ruta antes de reducir código; evitar nuevos motores/listeners y evaluar carga por feature. Beneficio de capacidad de respuesta; coste de perfilado y compatibilidad LS.

**Alternativas:** Desactivar por settings lo que no se usa, midiendo función y efecto.

**Dependencias:** Traza, scripts de plataforma/tema separados y escenarios de interacción.

**Riesgos:** Borrar unused JS de una sola navegación puede romper variantes y carrito después.

**Cómo verificar:** Traza con CPU móvil y acciones representativas; repetir si hay variación.

**Reutilización:** Presupuesto incremental y arquitectura común para todas las tiendas.

## IPN-013

**Identificador:** IPN-013 · **Fecha:** 2026-11-08

**Área:** Rendimiento / Imágenes

**Hallazgo:** sizes de cards y medios sobredimensionados merecen ajuste

**Evidencia:** item-image.tpl L87–100; [Lighthouse PDP](../13-evidence/measurements/lighthouse/pdp-mobile.json)

**Estado:** Confirmado

**Comportamiento actual:** Card declara 50vw desktop aun con cuatro columnas. Lighthouse estima oportunidades de entrega de imágenes, hasta ~95 KiB en la muestra PDP; no es ahorro obtenido.

**Problema u oportunidad:** La selección del recurso puede exceder el tamaño necesario para la tarjeta o medio.

**Impacto:** SEO 2/5; rendimiento 4/5; UX 3/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Pasar sizes según contenedor/columnas al helper y revisar imagen/logotipo entregados con DPR real. Beneficio de red/decodificación; coste medir y conservar calidad.

**Alternativas:** Reconfigurar archivos de medios adecuados antes de tocar lógica cuando el origen es el asset.

**Dependencias:** Ancho renderizado, srcset, currentSrc y Network.

**Riesgos:** Confundir naturalWidth con píxeles crudos o reducir de más en retina.

**Cómo verificar:** Comparar selección y bytes a DPR 1/2 y varios anchos, con calidad visual.

**Reutilización:** Extensión parametrizada del helper compartido, sin otra implementación.

## IPN-014

**Identificador:** IPN-014 · **Fecha:** 2026-11-08

**Área:** Rendimiento / Responsive

**Hallazgo:** Dos elementos de imagen responsive pueden competir por red

**Evidencia:** hero.tpl L50–95; blocks/slide.tpl L49–103; [análisis](../05-performance/image-loading.md)

**Estado:** Inferido

**Comportamiento actual:** Las ramas de arte desktop/mobile son imgs separados y mobile puede ser high priority oculto en desktop. No se configuraron ambas variantes para forzar una prueba durante discovery.

**Problema u oportunidad:** La arquitectura de dos img plantea una hipótesis de descarga que aún exige una configuración real para comprobarla.

**Impacto:** SEO 1/5; rendimiento 4/5; UX 3/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Evaluar art direction con un picture compartido y sources media en el helper existente. Beneficio potencial de red; requiere comprobar capacidades de medios y todos los callers.

**Alternativas:** Conservar estrategia actual si Network demuestra que solo carga el recurso útil en el caso real.

**Dependencias:** Medios desktop/mobile reales y prueba de red por componente.

**Riesgos:** Cambiar lazy o perder selección de formato puede empeorar LCP o dejar imágenes vacías al resize.

**Cómo verificar:** Distinguir solicitado/completado/decodificado/renderizado/visible; no inferir descarga desde DOM.

**Reutilización:** Patrón general, todavía no una mejora cuantificada de esta configuración.

## IPN-015

**Identificador:** IPN-015 · **Fecha:** 2026-11-08

**Área:** Arquitectura / Accesibilidad

**Hallazgo:** IDs repetidos en bloques y formularios del DOM

**Evidencia:** [inventario de duplicados](../13-evidence/measurements/browser/state-audit.json)

**Estado:** Confirmado

**Comportamiento actual:** Home: 14 grupos de IDs repetidos, incluidos ns-block-heading y variation_1; categoría/PDP también repiten variation_1. Hay clones de slider, pero no todo duplicado se atribuye a ellos.

**Problema u oportunidad:** Las relaciones por ID necesitan revisión, separando duplicación estática, formularios y clones.

**Impacto:** SEO 1/5; rendimiento 1/5; UX 4/5; mantenibilidad 5/5

**Severidad:** Media

**Solución recomendada:** Trazar la fuente de cada ID y sus consumidores antes de generar identificadores por instancia. Beneficio potencial para labels/selectores; se debe demostrar qué relaciones se afectan.

**Alternativas:** Usar scopes de componente al buscar nodos cuando el contrato existente lo permita.

**Dependencias:** block_attributes de plataforma, inputs y motor de slider.

**Riesgos:** Renombrar IDs sin actualizar for/ARIA/editor rompe relaciones; no hay prueba de fallo de cada duplicado.

**Cómo verificar:** Cruzar id/for/aria-controls y búsqueda JS con card repetida y clones.

**Reutilización:** Regla de identidad por instancia para componentes compartidos.

## IPN-016

**Identificador:** IPN-016 · **Fecha:** 2026-11-08

**Área:** CSS / Mantenibilidad

**Hallazgo:** La capa nativa de utilidades explica gran parte de !important

**Evidencia:** [medidas CSS](../05-performance/static-asset-measurements.md), [cascada](../03-editor/responsive-controls.md)

**Estado:** Confirmado

**Comportamiento actual:** CSS critical/utilities/async: 15/496/23 ocurrencias; también hay estilos inline por settings.

**Problema u oportunidad:** Los parches pueden escalar especificidad si se ignoran inline y utilidades del tema.

**Impacto:** SEO 1/5; rendimiento 2/5; UX 3/5; mantenibilidad 5/5

**Severidad:** Media

**Solución recomendada:** Modificar control/fuente responsable y acotar variantes antes de un override. Beneficio de mantenibilidad; no borrar utilidades nativas para bajar un contador.

**Alternativas:** Excepción !important justificada y documentada cuando el contrato externo la exige.

**Dependencias:** Estilo computado, origen de regla y alcance real.

**Riesgos:** Cambiar CSS global o moverlo a layers sin entender prioridad puede extender regresiones.

**Cómo verificar:** Inspeccionar cascada en los nodos afectados y comparar dispositivos.

**Reutilización:** Política compartida de estilo limpio, con branding por tienda.

## IPN-017

**Identificador:** IPN-017 · **Fecha:** 2026-11-08

**Área:** SEO / Datos estructurados

**Hallazgo:** JSON-LD WebPage inválido en la ruta 404

**Evidencia:** [rutas y parseo](../10-quality/runtime-page-audit.md), structured-data.tpl L175–221

**Estado:** Confirmado

**Comportamiento actual:** La sonda devuelve HTTP 404 correctamente, pero el objeto WebPage falla al parsear. El patrón de coma previa y breadcrumbs vacíos también se observó en password.

**Problema u oportunidad:** Una lista vacía deja un objeto de datos estructurados sintácticamente inválido.

**Impacto:** SEO 4/5; rendimiento 1/5; UX 2/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Serializar la lista sin coma dependiente de que haya breadcrumbs. Beneficio de consistencia sintáctica; revisar todas las ramas del snippet existente.

**Alternativas:** Omitir elementos inexistentes de forma válida, manteniendo Organization y el contenido permitido.

**Dependencias:** Twig/JSON-LD compartido y casos de lista vacía.

**Riesgos:** Agregar otro JSON-LD no corrige el bloque inválido y puede duplicar entidades.

**Cómo verificar:** JSON.parse de todos los scripts en 404, home, PDP, blog, búsqueda y páginas sin breadcrumbs.

**Reutilización:** Patrón de serialización aplicable a cualquier plantilla.

## IPN-018

**Identificador:** IPN-018 · **Fecha:** 2026-11-08

**Área:** SEO / Accesibilidad

**Hallazgo:** La 404 observada tiene title vacío

**Evidencia:** [matriz responsive](../10-quality/responsive-results.md), axe document-title de 404

**Estado:** Confirmado

**Comportamiento actual:** HTTP 404 y H1 existen, pero document.title está vacío; password inicial comparte esa carencia en otro contexto.

**Problema u oportunidad:** La página de error carece de un título documental útil.

**Impacto:** SEO 2/5; rendimiento 1/5; UX 3/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Revisar metadatos de plataforma para esa ruta y definir título útil por el mecanismo soportado. Beneficio para orientación/AT; no insertar otro title global.

**Alternativas:** Escalar a soporte de plataforma si head-tags no ofrece control para ese caso.

**Dependencias:** Componente privado head-tags y configuración disponible.

**Riesgos:** Una solución Twig global podría duplicar metadatos en todas las otras páginas.

**Cómo verificar:** HTML inicial contiene un único title útil en la 404 sin afectar otras rutas.

**Reutilización:** Criterio de QA reusable; solución depende de plataforma.

## IPN-019

**Identificador:** IPN-019 · **Fecha:** 2026-11-08

**Área:** SEO / Reutilización

**Hallazgo:** El tema ya emite JSON-LD de organización, página y producto

**Evidencia:** [tipos y condiciones](../04-seo/structured-data.md), HTML inicial del crawl

**Estado:** Confirmado

**Comportamiento actual:** Organization global, WebPage/BreadcrumbList, Product/Offer por contexto y Blog/BlogPosting ya están presentes.

**Problema u oportunidad:** Añadir otro generador sin inventario puede duplicar entidades y valores.

**Impacto:** SEO 4/5; rendimiento 2/5; UX 2/5; mantenibilidad 5/5

**Severidad:** Baja

**Solución recomendada:** Auditar coherencia antes de agregar plugins o schema manual. Beneficio de evitar señales duplicadas sin bytes nuevos; requiere revisar apps instaladas, todavía no auditadas en Admin.

**Alternativas:** Agregar únicamente un tipo pertinente ausente, con datos verificables y semántica definida.

**Dependencias:** Estado de apps y requisitos vigentes del buscador.

**Riesgos:** Inventar reseñas/ratings/precio o prometer rich results no respaldados.

**Cómo verificar:** Comparar entidades por URL/ID y valores visibles; validadores separados de JSON.parse.

**Reutilización:** Playbook común que evita repetir desarrollo SEO innecesario.

## IPN-020

**Identificador:** IPN-020 · **Fecha:** 2026-11-08

**Área:** SEO / Lanzamiento

**Hallazgo:** La protección de tienda cambia el acceso del rastreador

**Evidencia:** [sin sesión](../13-evidence/measurements/http/route-probes.json), [robots con sesión](../13-evidence/measurements/crawl/robots.txt)

**Estado:** Confirmado

**Comportamiento actual:** Sin sesión hubo password; con sesión, robots/sitemap accesibles. Robots declara restricciones de cuenta, búsqueda, carrito y preview. CDN gzip rechazó al cliente HTTP de auditoría con 403.

**Problema u oportunidad:** Las pruebas con sesión no acreditan cómo podrá rastrear la tienda un visitante sin acceso.

**Impacto:** SEO 5/5; rendimiento 1/5; UX 2/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Antes del lanzamiento repetir endpoints sin sesión y verificar acceso de buscadores, manteniendo la protección hasta que el propietario decida publicar. No tratar el estado intencional de password como una avería.

**Alternativas:** Validación de lanzamiento en una ventana autorizada y Search Console del propietario.

**Dependencias:** Decisión comercial y control de plataforma.

**Riesgos:** Quitar contraseña para probar expone la tienda; un 403 de esta herramienta no prueba bloqueo de Googlebot.

**Cómo verificar:** GET sin cookies, respuesta final y sitemap/robots reales al lanzar.

**Reutilización:** Puerta de verificación para todas las tiendas, sin cambios durante discovery.

## IPN-021

**Identificador:** IPN-021 · **Fecha:** 2026-11-08

**Área:** Motion / Accesibilidad

**Hallazgo:** Reduced-motion no cubre todas las animaciones opcionales

**Evidencia:** [motion nativo](../06-motion/native-animations.md), critical.css L328/L355 y store.js L3958

**Estado:** Confirmado

**Comportamiento actual:** Hay protección de hero/slideshow/utilidades y parallax, pero no se comprobó una política integral para marquee/loaders/autoplay.

**Problema u oportunidad:** No se dispone de evidencia de cobertura integral de motion accesible en todos los efectos.

**Impacto:** SEO 1/5; rendimiento 2/5; UX 4/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Revisar cada efecto activado y ofrecer alternativa estática/pausa cuando corresponda. Beneficio de lectura/control; coste bajo de CSS y mayor si requiere cambiar motor.

**Alternativas:** No activar efectos sin valor UX demostrado.

**Dependencias:** Settings reales y comportamiento de los motores existentes.

**Riesgos:** Deshabilitar todo sin considerar feedback de carga o estado puede quitar información.

**Cómo verificar:** Reduce al cargar/cambiar preferencia, foco, teclado y autoplay con datos reales.

**Reutilización:** Tokens/política de motion compartidos, efectos concretos por tienda.

## IPN-022

**Identificador:** IPN-022 · **Fecha:** 2026-11-08

**Área:** Reutilización / Licencias

**Hallazgo:** No hay licencia de tema encontrada que autorice una biblioteca entre tiendas

**Evidencia:** [inventario](../01-architecture/directory-map.md), [multitienda](../08-design-system/multi-store-strategy.md)

**Estado:** No comprobado

**Comportamiento actual:** Se tiene autorización de inspección de este proyecto; no se encontró licencia del tema en su raíz ni permiso de transferencia de implementación.

**Problema u oportunidad:** La autorización de inspección no resuelve el permiso de distribución entre comerciantes.

**Impacto:** SEO 1/5; rendimiento 1/5; UX 2/5; mantenibilidad 5/5

**Severidad:** Media

**Solución recomendada:** Compartir metodología/contratos y código propio con procedencia registrada; verificar derechos antes de distribuir archivos del tema. Beneficio de sostenibilidad; limita la copia directa, no la investigación.

**Alternativas:** App propia con interfaces oficiales o patrones implementados de forma independiente.

**Dependencias:** Permisos/licencias del titular, assets y terceros por separado.

**Riesgos:** La licencia de Craft Anything no se extiende a Ipanema o marcas del comerciante.

**Cómo verificar:** Registrar fuente y permiso de cada unidad que se quiera distribuir.

**Reutilización:** Arquitectura de conocimiento portable sin confundirla con licencia de código.

## IPN-023

**Identificador:** IPN-023 · **Fecha:** 2026-11-08

**Área:** Editor / Configuración

**Hallazgo:** Los valores efectivos pueden ser de sección y no globales

**Evidencia:** settings_data.json pagination classic; templates/pages/category.json pagination infinite; [matriz](../02-native-components/settings-matrix.md)

**Estado:** Confirmado

**Comportamiento actual:** El mismo concepto existe en capas distintas; cambiar un setting global no garantiza modificar una sección que guarda su propio valor.

**Problema u oportunidad:** Un ajuste en la capa equivocada puede no producir el cambio o borrar una elección de instancia.

**Impacto:** SEO 2/5; rendimiento 2/5; UX 3/5; mantenibilidad 5/5

**Severidad:** Media

**Solución recomendada:** Registrar fuente efectiva, default de schema y fallback Twig antes de tocar CSS. Beneficio de cambios más pequeños y reversibles; coste de rastrear la instancia.

**Alternativas:** Configurar la instancia desde editor cuando el control existe, sin cambiar código.

**Dependencias:** Schema del padre/bloque y datos guardados actuales.

**Riesgos:** Sobrescribir datos para uniformar una tienda puede borrar decisiones del comerciante.

**Cómo verificar:** Seguir valor guardado → Twig → clases/estilos computados.

**Reutilización:** Método determinista de personalización para todas las tiendas.

## IPN-024

**Identificador:** IPN-024 · **Fecha:** 2026-11-08

**Área:** Responsive / JavaScript

**Hallazgo:** Inicialización por ancho merece comprobarse tras resize

**Evidencia:** store.js L175–186, L318–324, L368–371; [galerías](../07-commerce/carousels-and-galleries.md)

**Estado:** Inferido

**Comportamiento actual:** Varias ramas hacen return según innerWidth al inicializar. La matriz prueba cargas independientes; no demuestra reconstrucción correcta al cruzar todos los cortes.

**Problema u oportunidad:** Un layout correcto tras recarga puede tener estado interactivo incorrecto después de cruzar un corte.

**Impacto:** SEO 1/5; rendimiento 2/5; UX 3/5; mantenibilidad 4/5

**Severidad:** Media

**Solución recomendada:** Probar orientación/resize y definir destroy/reinit solo donde falle el contrato existente. Beneficio de consistencia; evita dos copias del contenido, pero exige cleanup.

**Alternativas:** CSS responsive con scroll nativo si cubre el caso sin estado de motor.

**Dependencias:** Instancias Swiper, listeners y datos de configuración.

**Riesgos:** Reinicializar indiscriminadamente puede duplicar sliders o perder posición/foco.

**Cómo verificar:** Secuencia 390→768→390 y 1024→767, inspeccionando instancia, visibilidad y recursos.

**Reutilización:** Contrato de ciclo de vida para módulos reutilizables.

