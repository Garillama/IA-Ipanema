# RHINO — correcciones locales de accesibilidad

Fecha: 2026-11-10T20:40:02.183855+00:00. Proyecto `rhino-performance`. Tema local correcto `~/Escritorio/Cli/Rhino-Ipanema`.

**Estado: candidato aplicado localmente, QA parcial aprobado. No publicado.** No es una nueva medición de Lighthouse de producción ni una certificación WCAG. Se conservó el trabajo previo del tema, que ya tenía modificaciones y archivos sin seguimiento.

## Cambios

| Archivo del tema | Corrección |
|---|---|
| `blocks/product-rating.tpl` | Nombre desde texto visible; etiqueta opcional como title |
| `sections/bundle-builder.tpl` | Nombre accesible del filtro; retirada de outline:none inline |
| `sections/google-reviews.tpl` | Logo role=img, contraste y estados/relación de Leer más |
| `sections/category-tabs.tpl` | H1 de categoría con ajuste explícito de coexistencia |
| `snippets/bundle/bundle-builder-js.tpl` | Controles nativos, etiquetas, foco tras rerender; lógica de selección intacta |
| `snippets/bundle/bundle-builder-styles.tpl` | Contraste y retirada de supresión de foco |
| `snippets/modals/modal.tpl` | Cerrar/Anterior con nombre y type=button |
| `snippets/footer/footer-rhino.tpl` | Wrapper interior div; se conserva footer nativo exterior |
| `snippets/product/product-video-item.tpl` | Nombre en ambos enlaces de reproducción |
| `snippets/product-list/product-item/item.tpl` | Retirada del aria-label que sustituía el texto visible |
| `static/css/style-critical.css` | Contraste grid/PDP sin opacidad reductora |
| `static/css/style-async.css` | Contraste de colección y productos del blog |

No se modificaron templates, settings_data, traducciones, catálogo, precios, JSON-LD, carrito ni endpoints. El cambio del pack conserva el cuerpo de `selectProduct` exactamente; cambia la semántica y el cableado de foco/teclado, no sus cálculos. Se quitaron supresiones de foco existentes; no se aumentó el número de declaraciones `!important` ni se creó otro motor de modal, carrusel o compra.

El color secundario y los descuentos se oscurecen en sus declaraciones fuente. Los ajustes claros de PDP/blog/packs se limitan con `color-mix` sobre las superficies claras observadas; se conservan fallbacks. Eso puede cambiar la jerarquía visual: requiere revisión visual completa antes de publicar. No garantiza contraste si se cambia a un fondo oscuro. [Referencia de color-mix](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix).

### Regla de H1

Hoy `page-header` está deshabilitado en la plantilla de categoría. `category-tabs` usa el nombre real de la categoría como H1. Si se habilita el header nativo, hay que desmarcar **Usar el nombre de categoría como H1** en las pestañas. Se probaron ambos escenarios válidos y se detecta el inválido con ambos propietarios activos; no se afirma que la plataforma impida esa configuración automáticamente. No se editó ningún JSON protegido para activar/desactivar secciones.

## Comparación y pruebas reales

- Navegador Chrome local, red bloqueada, seis anchos: 360, 390, 768, 1024, 1440 y 1920 px.
- Fixture antes: ocho reglas axe con violaciones reproducidas; después: cero violaciones detectadas de las reglas seleccionadas. `label-content-name-mismatch` conserva nodos incompletos: no equivale a una aprobación completa de esa regla ni de WCAG.
- Dos landmarks `contentinfo` antes; uno después en el árbol AX del fixture.
- Packs: Enter y Espacio llaman una sola vez a la selección; el selector ya no es secuestrado por el keydown del contenedor. Cambio de variante sin selección adicional; se conserva el foco en el control equivalente tras regenerarlo y no se roba el foco de un control externo.
- El botón de cierre no envía el formulario de prueba. Los modales nativos admiten formulario opcional: se conserva su contenido/submit; únicamente cierre/regreso/título llevan `type=button`.
- Leer más sincroniza `aria-expanded` true/false, `aria-controls` apunta al texto y los IDs dinámicos son únicos en la instancia probada.
- Contraste de los tokens configurables probados también con blanco personalizado: sin violaciones ni comprobaciones incompletas en ese grupo concreto.
- 54 comprobaciones estáticas aprobadas: hashes, JSON schema, selección nativa inalterada, traducciones usadas en cuatro idiomas, ausencia de nuevos important y propiedad del H1. Sintaxis JavaScript comprobada con sustitución explícita de expresiones Twig, sin presentarla como compilación de Tiendanube.
- Inventario estático completo del tema: `json_schema_errors=[]`.
- Integridad: 384 archivos de fuente en el baseline; únicamente los 12 declarados cambiaron. El contenido aplicado coincide byte a byte con el candidato revisado.

**Límite de la prueba:** el navegador ejecutó fragmentos derivados del código y los `renderProduct`/`renderCatalog` reales con dependencias comerciales sintéticas. No es el render Twig completo ni una prueba de carrito real. Las capturas son del fixture, no una comparación visual de toda la tienda. No existe una URL remota que incorpore estos archivos locales; repetir PageSpeed de producción no mediría este parche.

## Consejo y revisión

Claude y Codex produjeron propuestas independientes, contraste y respuestas: seis invocaciones reales válidas, modelos equilibrados del registro (`claude-sonnet-5-5`, `gpt-6.1-sol`, esfuerzo medium). Se resolvió ampliar el candidato para incluir contraste y H1, conservando la separación de los packs para su reversión. Dos preparaciones iniciales de defensa fallaron antes de iniciar proveedor por metadatos `requested_agent` omitidos en el helper local; se corrigió ese helper y se conservaron propuestas/contrastes. No se cambió el motor ni se ejecutó CommandCode.

Claude revisó después el diff y los recibos del controlador en una séptima invocación real: `approve` **para el candidato local**, con controles de staging pendientes. El controlador contrastó sus afirmaciones con la fuente: el modal sí puede contener un formulario; no se toma la frase del revisor en sentido contrario como evidencia. La inicialización de reseñas tiene un ancestro data-section-id en la fuente actual; otros montajes deberán comprobarlo. La revisión de un modelo no sustituye QA.

[ADR](ADR-RHINO-003.md) · [Resumen verificable](accessibility-fixes.json).

## Evidencia y reproducción

[Diff exclusivo de este trabajo](../runs/rhino-performance/20261110T204833-a11y-correct-theme-root-6d9be679/accessibility.patch) · [QA de componentes](../runs/rhino-performance/20261110T204833-a11y-correct-theme-root-6d9be679/component-qa.json) · [QA estático](../runs/rhino-performance/20261110T204833-a11y-correct-theme-root-6d9be679/static-qa.json) · [Revisión independiente](../runs/rhino-performance/20261110T204833-a11y-correct-theme-root-6d9be679/independent-review.json) · [Integridad](../runs/rhino-performance/20261110T204833-a11y-correct-theme-root-6d9be679/integrity-after.json).

Los originales, backups y snapshots quedan en los directorios locales ignorados por Git; el patch es exclusivo de esta tienda, sin autorización para redistribuir su código a otros clientes.

Desde la raíz del agente:

```bash
node tests/browser/rhino_accessibility.mjs reports/runs/rhino-performance/20261110T204833-a11y-correct-theme-root-6d9be679
```

El comando exige los snapshots antes/candidato del run. No consulta Google ni la tienda y termina con código distinto de cero si falla una comprobación. Reproduce la prueba de componentes, no sustituye un entorno Tiendanube.

Transacciones locales con backup: `b2c61e09f82a450eb778b703b2331509` y `754b0d28bf5d400296d2b36f150ae09e`. Permanecen aplicadas; no se registran como solución global verificada ni como liberación completa. Para revertir, usar el mecanismo `attempt revert` correspondiente con comprobación de hashes; nunca reset/clean ni sobrescritura de cambios posteriores.

## Pendientes que no se ocultaron

1. Lista inválida del artículo: pertenece al contenido del CMS. No se inyectó un limpiador JS ni se modificó el contenido remoto. Requiere una edición editorial autorizada del artículo y nueva comprobación.
2. Render Twig real de Tiendanube, consumidores completos, staging, galería/video, menú/foco/Escape, carrusel completo y revisión visual. No se publicó para obtener esas pruebas.
3. H1 de contenido de home, overflow y retorno de foco nativo del menú: siguen requiriendo una decisión/prueba específica; no se introdujeron arreglos globales especulativos.
4. Revisión humana con lector de pantalla y superficies de branding distintas; los tests automatizados no certifican AA.
5. No se midió un nuevo score público ni una mejora de LCP/INP: el sitio remoto sigue sin estos cambios locales.

## Corrección de ubicación — 10 de noviembre de 2026

La primera aplicación se hizo por error en `~/Escritorio/Rhino-Ipanema`. El propietario indicó que la copia de trabajo correcta es **`~/Escritorio/Cli/Rhino-Ipanema`**. Se corrigió el registro local ignorado por Git.

Antes de trasladar se compararon los 12 archivos: cinco divergían de la copia inicial. Se preservaron la clase close-all del overlay, el CSS trasladado a critical para evitar cambios durante la carga, y las mejoras actuales del pack (normalización de variantes, cantidades, UUID, envío al carrito y paginación). Las correcciones de contraste de la colección se aplicaron en critical, donde esta copia contiene sus reglas; no se reintrodujeron en async.

Se repitieron las pruebas de componentes y las 54 comprobaciones estáticas sobre el candidato de la carpeta correcta. Claude realizó una revisión independiente adicional y aprobó el candidato local, con las mismas restricciones de render real/staging. Se reutilizó el ADR previo; no se fingió una nueva deliberación completa. El controlador comprobó que el contenido aplicado coincide con el revisado.

Después se revirtieron únicamente las dos transacciones propias de la carpeta equivocada, con comprobación de hashes. No se usaron reset/clean ni se descartaron cambios ajenos. La carpeta correcta quedó con 12 archivos modificados. **No se ejecutó push ni sincronización remota.** Los registros anteriores se conservan en el run original; la evidencia enlazada arriba corresponde ahora a la copia correcta.
