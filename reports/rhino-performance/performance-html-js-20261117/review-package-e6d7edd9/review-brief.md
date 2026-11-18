# Paquete de revisión independiente — candidato hero

Candidato: `e6d7edd9bb3590b0909cd71a9245bf5a92cbd7034f24fc57bb00389d0ec3f841`  
Estado: **needs_evidence**. Esta revisión, si se autoriza y ejecuta, será externa al gate del controlador y no contará por sí sola como aprobación de este.

## Alcance congelado

El paquete contiene el diff exacto y los dos archivos candidatos completos: `sections/hero.tpl` y `snippets/image.tpl`. También incluye la configuración actual de home, captura HTML desktop autorizada previamente, análisis comparativo offline, prueba de navegador y resultados de sus 231 aserciones, además de la ficha local del helper de imágenes.

## Evidencia de producción ya conservada

No se hicieron solicitudes nuevas para este paquete. La captura desktop existente fue HTTP 200, cuerpo HTML inicial de 1,174,783 bytes descomprimidos y 111,853 bytes transferidos (Brotli). Hash del cuerpo: `7da336fc86f03ba9d618000d3d4ea56125e2b1cc4957f8495a91b671f1852fc8`.

En esa respuesta la hero desktop tenía GIF transparente como `src`, `data-srcset` en lugar de `srcset`, clase `lazyload` y ninguna prioridad alta. La hero móvil llevaba `src/srcset` activo y prioridad alta, aunque estaba oculta visualmente en escritorio. El análisis de las solicitudes registró descarga de ambas variantes en la captura desktop. Auditoría Lighthouse previa: recurso desktop de LCP no descubierto a tiempo en 5/5 mediciones; la captura previa es evidencia histórica, no medición posterior al candidato.

La configuración preservada en `config/home-hero.json` mantiene la sección hero primera (`hero_1794546525965`), imagen desktop `@media-lib:95cbfc17-3ab4-4e7c-bb93-b8c1afd06717`, alternativa móvil habilitada `@media-lib:fc9598f3-4bc6-437f-9f2a-641ff6d0d0ad`, altura 80 y `auto_height=false`. `templates/pages/home.json` no cambia en el parche.

## Pruebas sintéticas conservadas (no repetir)

`hero-responsive-browser-results.json` registra 32 escenarios, 231 aserciones y siete anchos: 360, 390, 412, 768, 1024, 1440 y 1920 px. Casos: ambas imágenes, desktop solamente, móvil solamente, sin imagen, hero prioritaria y posterior diferida. Las respuestas fueron interceptadas en `fixtures.invalid`; no se hizo red externa. En el fixture cada caso selecciona una sola fuente/solicitud; ratios observados 0.82 móvil y 2.133 escritorio, CLS 0; `alt` se conserva. La carga posterior usa el bundle local de LazySizes y `unveil` forzado.

Límite: el fixture no ejecuta el renderer Twig/Liquid real de Tiendanube. No prueba el HTML final generado, los datos reales de `resolve_media`, la carga lazy natural ni el comportamiento visual remoto. No se ha medido Lighthouse después del candidato.

## Contratos y dependencias

- `snippets/image.tpl` es compartido. La rama nueva solo se activa cuando el caller entrega `image_mobile_src`; las llamadas preexistentes no lo pasan, según el análisis estático local. El helper anterior permanece en la rama `else`.
- `resolve_media` es un filtro/plataforma de Tiendanube, no implementado por el tema. El contrato local documentado en `contracts/image-loading.md` y consumido por el helper expone `type`, `sourceUrl`, `sourceWidth`, `sourceHeight`, `altText` y `srcSets` con formatos y tamaños. La semántica del renderer y el caso de referencias no procesadas requieren validación nativa; no se deben inferir a partir del fixture.
- `static/js/libraries-standalone.js` SHA256 `da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34`. El bundle configura LazySizes con `lazyClass=lazyload`, `srcsetAttr=data-srcset` y `loadHidden=true`. Su loader mueve `data-srcset` a `srcset` y en `<picture>` también activa `data-srcset` de los `<source>` al revelar el `<img>`. En el candidato, la primera hero usa fuentes activas en HTML inicial y no `data-srcset`; las posteriores conservan `loading=lazy` y la clase de LazySizes, pero sus fuentes quedan activas para permitir selección responsive. Esto no demuestra que LazySizes no altere la selección en todos los navegadores; verificar en QA nativo.
- AVIF/WebP se ofrecen solo para los `srcSets` entregados por `resolve_media`; después se emite la fuente original como fallback. Debe verificarse que la plataforma emita esos formatos y URLs para ambos assets de la hero.
- El art direction usa un único `<picture>` y `<img>`/`alt`; fuentes móvil con media query primero, desktop como fallback. Los `width`/`height` de cada `<source>` pretenden reservar la proporción de la variante elegida. Renderer y layout shift real siguen pendientes.
- La sección conserva los controles del editor en `hero.tpl`; no se modifican schema ni `home.json`. El archivo compartido `snippets/image.tpl` es el riesgo de regresión de mayor alcance y debe revisarse contra consumidores existentes.

## Preguntas para Claude y Codex

Responder con evidencia de archivo/función, separando defecto reproducible, riesgo con fundamento y verificación Tiendanube pendiente:

1. ¿Es aceptable modificar `snippets/image.tpl` compartido? ¿El guard opt-in preserva realmente contratos de callers antiguos?
2. ¿`image_mobile_src` colisiona con parámetros existentes o existe un helper reusable para art direction?
3. ¿El orden de `<source>` conserva AVIF, WebP y fallback original para móvil y escritorio, incluidos medios no procesados/no imagen?
4. ¿La hero prioritaria se descubre en HTML inicial sin depender de JavaScript? ¿Existe algún camino de plantilla donde siga generándose lazy markup?
5. ¿LazySizes puede alterar o demorar la selección de la hero posterior? Distinguir comportamiento del bundle de lo no probado por fixture.
6. ¿Las dimensiones por `<source>` y la ausencia de dimensiones en `<img>` previenen CLS de forma compatible con el renderer? Revisar fallback/compatibilidad.
7. ¿Son correctos desktop-only, mobile-only, sin imagen, first hero y banners posteriores?
8. ¿Se preservan schema y atributos de editor Ipanema?
9. ¿Qué riesgos concretos de Twig/Liquid/renderizado quedan que no cubren las fixtures?

No asumir que un cambio de helper compartido es incorrecto por sí solo. Citar consumidor/contrato y efecto observado.

## Contexto del gate central

La ruta soportada del consejo está en `tools/ia.py orchestrate ... --execute`. En el engine, `execute()` invoca `central_qa()` antes de `run_council()` (`tools/ipanema/orchestration/engine.py`). Para scope `workspace`, `central_qa` crea vista aislada sin red y ejecuta `python3 -m unittest discover -s tests/unit -v` con timeout 180 s. El intento previo conservado ejecutó 436 pruebas (11 omitidas) y fue interrumpido antes de completar las intervenciones de ambos agentes. Para scope `theme`, central QA ejecuta `tools/audit_source.py` sobre el snapshot del tema completo; no es un selector de pruebas focalizadas. No hay flag CLI para evitar o focalizar ese paso. No se llamó a los agentes en esta etapa porque no existe una ruta independiente soportada que evite este gate sin modificar engine/políticas o bypass del controlador.

## Estado y opciones

- Claude independiente: pendiente; no llamado para este hash.
- Codex independiente: pendiente; no llamado para este hash.
- Validación nativa Tiendanube: pendiente; no se envió POST.
- Storefront: sin solicitudes nuevas; sin cambios remotos.

A. Autorizar una única ejecución del consejo existente con su QA central obligatorio, sabiendo que scope=workspace ejecutará la suite completa; una revisión externa no garantiza pasar el gate.

B. Mantener el gate operativo intacto y autorizar primero el diseño de una capacidad de QA focalizado revisable en el controlador. No se implementó ni usó una ruta alterna en esta fase.

Después de revisiones válidas y resolución de objeciones, la validación nativa sin persistencia de solo estos dos archivos requerirá una autorización separada para POST al validador de Tiendanube. No se incluye aquí autorización de POST ni publicación.
