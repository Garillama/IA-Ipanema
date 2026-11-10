# RHINO — primer parche local de rendimiento

Fecha: 2026-11-10T21:38:30.704536+00:00. Carpeta correcta: **`~/Escritorio/Cli/Rhino-Ipanema`**.

**Estado: implementación parcial, aplicada localmente. Sin push ni publicación.** Se corrigió el descubrimiento inicial de la primera portada del blog usando el componente nativo. El nuevo LCP de la tienda no se ha medido porque estos archivos aún no están publicados ni existe aquí un renderer Twig completo.

## Qué cambió

| Archivo | Cambio |
|---|---|
| `snippets/blog-card.tpl` | Nuevo parámetro opcional `card_image_priority_high`, default false, enviado al helper nativo tanto en portada como placeholder. |
| `sections/main-blog.tpl` | Prioridad solo en la primera card con imagen, plantilla blog, vista normal y sin filtro `tag`. |
| `sections/blog-carousel.tpl` | False explícito para conservar lazy y evitar herencia de prioridad. |
| `sections/blog-post-related.tpl` | False explícito en artículos relacionados. |
| `sections/home-news.tpl` | False explícito en noticias de home, consumidor adicional encontrado al comprobar dependencias. |

No se creó un helper, motor, biblioteca, preload ni JavaScript nuevo. El helper `snippets/image.tpl` ya anula lazy/lazy_js y emite `src`/`srcset` y `fetchpriority=high`. El CSS existente `.fade-in.image-priority-high` ya hace visible esa imagen. Enlaces, alt, datos estructurados, fuentes, estilos, comercio y orden de contenido permanecen fuera del diff. Las anteriores12correcciones de accesibilidad se conservaron.

La condición de posición se comprobó para la composición actual: page-header deshabilitado, main-blog primera sección activa y primera card observada en viewport en las tres muestras móviles previas. Si el editor antepone otras secciones, hay que revalidar el elemento LCP y esta prioridad; no se inventó un contrato de section.index.

## Antes/después comprobado

| Propiedad | Antes | Candidato |
|---|---|---|
| Primera portada, HTML proyectado | Solo atributos lazy/data-srcset | src/srcset y prioridad alta nativa |
| Peticiones de imagen sin JS en fixture normal | 0 | 1, la primera portada |
| Opacidad de primera portada sin JS | 0 | 1 |
| Prioridad de solicitud observada en Chrome | Sin solicitud | High |
| Otras portadas, fragmento view=cards, filtros, otros consumidores | Diferidas | Diferidas |
| Geometría en seis anchos del fixture | Baseline | Invariante |
| Peso del JPG original | Aproximadamente500KB | **Sin cambio** |
| LCP real del blog | Baseline mediano13.26s | **No medido** |

**No se afirma que LCP bajó de13.26s a otro valor**, ni que se haya reducido el peso de la portada. La fixture usa SVG sintético para comprobar el comportamiento del navegador; no es el JPEG del comerciante ni la tienda renderizada por Tiendanube.

## Pruebas y revisión

- **35 checks estáticos**: ramas/contextos, default false, cuatro consumidores localizados, ambos tipos de imagen, helper y CSS nativos, hashes, schema intacto y posición actual respaldada por la evidencia anterior.
- **138 checks de navegador,29casos**: 360/390/768/1024/1440/1920px, portada/placeholder, sin JS, página2, view=cards, tag, imágenes deshabilitadas y otra plantilla. Solo loopback, sin solicitudes de tienda/API.
- Peticiones reales de la fixture vía Chrome DevTools Protocol; no se dedujo descarga por presencia DOM. Sin peticiones de otras portadas ni conexiones externas.
- Auditoría estática completa del tema: `json_schema_errors=[]`; `git diff --check` sin errores.
- El contenido aplicado coincide con el candidato revisado; únicamente los5archivos declarados cambiaron respecto al snapshot de esta tarea.

Claude y Codex hicieron propuestas independientes, contraste y defensa con contratos nativos válidos (seis invocaciones). Ambos retiraron la reescritura de fuentes por falta de beneficio incremental demostrado. El controlador resolvió con pruebas las objeciones de fade-in, composición actual y fragmentos, y amplió el alcance a home-news al descubrir ese consumidor.

Claude revisó independientemente el diff y los recibos y aprobó **conservar el candidato local**. Su resumen decía false en cuatro consumidores; la comprobación de fuente precisa el alcance real: tres consumidores llevan false literal y main-blog la condición explícita. No se tomó esa frase como sustituto del diff.

El primer intento de revisión posterior falló por sintaxis JSON. Se recuperó usando el contrato nativo existente y el controlador exigió decision=approve y changes=[]; no se modificó el orquestador ni se reparó una respuesta ambigua para aprobarla. Total de esta fase: 8 invocaciones reales; subtotal de coste informado por Claude$2.0380, sin inventar factura de Codex.

La primera ejecución del test asumía naturalWidth1200; Chrome corrige esa dimensión por densidad de srcset. Se corrigió la asunción del test para exigir imagen completada con dimensión positiva y opacidad1, no se alteró el parche para acomodarlo. El resultado fallido se conserva por separado.

[Diff propio](../runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f/performance.patch) · [QA estático](../runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f/static-qa.json) · [QA navegador](../runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f/browser-qa.json) · [Revisión independiente](../runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f/independent-native-review.json) · [Integridad](../runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f/integrity-after.json) · [Resumen](performance-fixes.json) · [ADR](ADR-RHINO-005.md).

## Reproducción

```bash
python3 tests/browser/prepare_rhino_blog_performance.py --run reports/runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f --baseline-run reports/runs/rhino-performance/20261110T205329-postpush-accessibility-7f9a46ef --applied
node tests/browser/rhino_blog_performance.mjs reports/runs/rhino-performance/20261110T212214-performance-local-implementation-142edc2f
```

Los snapshots y originales quedan locales, ignorados por Git; los comandos requieren esos artefactos. El evaluador de expresiones es restringido y vinculado al source: no se presenta como motor Twig. [Referencia oficial del contexto params GET](https://docs.tiendanube.com/help/layouts). Los casos de la plataforma siguen pendientes de render real.

## Pendientes reales

1. **Portada de500KB:** optimizar el archivo del CMS y verificar qué transformaciones soporta ese origen. No se añadieron URLs ni parámetros CDN inventados ni imágenes específicas hardcodeadas en el tema. Eso requiere trabajo de asset/CMS aparte.
2. **JavaScript/marketing:** el contrafactual redujo TBT pero empeoró LCP. Falta un ensayo que preserve eventos/atribución y comercio; no se cambió GTM, Meta, TikTok ni JS nativo.
3. **Video/CLS:** sigue faltando un mecanismo demostrado y una prueba con reproductor funcional. No se cambió autoplay ni se eliminó contenido para subir el score.
4. **Fuentes/CSS:** ya existe preload equivalente; no se reescribió la carga sin demostrar un beneficio. La cadena crítica queda en diagnóstico.
5. **Validación posterior:** render real de Tiendanube y red/currentSrc, filtros/paginación/carruseles, SEO/a11y y3–5muestras equivalentes del candidato. La URL pública mediría todavía la versión publicada, no este parche local.

Transacción con backup: `b9df038077aa45b8b4e45474eff5592c`. Permanece aplicada con QA parcial; no se registra como solución global verificada. Reversión solo mediante el intento propio y verificación de hashes, sin reset/clean. No se editó la carpeta equivocada, ni templates/configuración remota, ni producción.

## Verificación posterior al push del propietario

El parche se comprobó en la tienda publicada: [mediciones y límites](blog-release-validation.md). El LCP móvil mediano pasó de13.26a6.19s; Performance44a48. El rendimiento sigue parcial. El estado «no publicado» de las secciones anteriores describe la fase local original; el push posterior fue del propietario.
