## Revisión independiente

**Paquete:** SHA256 `c10cec1d30ff6f609e4f47378f313bb3b89fa034c84087e4a2fb7cef21172123` — coincide.  
**Diff:** SHA256 `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b` — coincide.

### Objeción confirmada

**H1 — La carga diferida de las hero posteriores mezcla LazySizes con carga nativa**  
**Severidad: MEDIUM**  
**Archivo:** `sections/hero.tpl`, inclusión del helper para hero responsive posterior.

El caller asigna `image_classes: 'fade-in lazyload'` e `image_lazy_js: false`. En `snippets/image.tpl`, `image_lazy_js: false` produce atributos `src/srcset` normales y `loading="lazy"`, pero `image_classes` conserva la clase `lazyload`. Así, el elemento lleva a la vez el marcador que activa LazySizes y la ruta de carga nativa.

El resultado sintético no resuelve esta interacción: el propio paquete deja pendiente comprobar el momento real de carga de LazySizes. No puedo afirmar que siempre provoque una descarga prematura, pero el contrato es contradictorio y puede alterar la carga o el fade-in.

**Corrección recomendada:** para esa rama, pasar solo `fade-in` y mantener `loading="lazy"` nativo; o usar el mecanismo completo de LazySizes con `data-src/srcset`. La primera opción coincide mejor con la intención del candidato de no depender de JavaScript para cargar la imagen.

### Revisión de D1, D2, R1 y R4

- **D1 — corregido estáticamente:** si solo hay imagen móvil válida, `hero.tpl` la pasa como `image_src` de una inclusión de imagen única. Los fixtures afirman una solicitud para ambos grupos de viewport.
- **D2 — corregido estáticamente:** el helper marca referencias `@media-lib:` no resueltas como inválidas y las excluye del renderizado final. Falta confirmar el contrato real y los valores que devuelve `resolve_media`.
- **R1 — corregido estáticamente:** con una imagen desktop inválida y móvil válida, `hero.tpl` entra en la rama de imagen móvil única.
- **R4 — corregido condicionalmente:** el helper conserva los `srcSets` originales cuando `resolve_media` los proporciona; si faltan, cae a `sourceUrl`. No está validado con respuestas reales del servicio de imágenes de Tiendanube.

### Otros puntos revisados

- **Ubicación y duplicación:** usar `snippets/image.tpl` reutiliza el componente de imágenes existente y la nueva rama requiere `image_mobile_src`. Sin embargo, la validación de URLs se repite en hero y helper. Es una duplicación de mantenimiento, no un defecto que justifique por sí solo otro componente.
- **Consumidores compartidos:** los siete archivos de contexto no muestran la nueva llamada de art direction. Aun así, `image_source_invalid` cambia el comportamiento general de referencias de medios inválidas; conviene verificar esos casos con los consumidores reales.
- **`srcset` de URLs directas:** el helper genera anchos distintos a partir de la misma URL cuando no hay objeto de medios. Eso da descriptores que no representan variantes de imagen. Es un riesgo para la ruta de URLs directas, aunque no demuestra una regresión del flujo habitual `image_picker`.
- **Alt móvil:** el `<img>` de un `<picture>` conserva un solo `alt`, tomado de la imagen desktop; `image_mobile_alt` se calcula y pasa, pero no se usa en esa rama. Si las variantes tienen contenido semántico distinto, la descripción puede ser incorrecta.
- **Selección responsive y prioridad:** el orden mobile-first de `<source>`, `sizes="100vw"` y prioridad alta únicamente en la sección considerada prioritaria son coherentes en el código. No he confirmado su resultado de red ni el `currentSrc` tras renderizar Twig.
- **Dimensiones y CLS:** la rama de art direction pone dimensiones en `<source>` y omite dimensiones y `aspect-ratio` del `<img>`. Puede reservar proporción por variante en navegadores compatibles, pero `auto_height` y el CLS real siguen sin prueba de plataforma.
- **Editor y Twig:** la composición mantiene la sección existente y no cambia el schema del editor. La validez de filtros, objetos y atributos depende del renderizador Tiendanube, que no se ha ejecutado.

La evidencia histórica respalda que en una navegación desktop se descargaron ambas variantes y que la imagen LCP se descubrió tarde. No demuestra una mejora posterior al candidato. Los fixtures tampoco equivalen a renderizado de Tiendanube.

**Dictamen: `changes_requested`**, por la mezcla de LazySizes y `loading="lazy"` en las hero posteriores. Los demás puntos descritos son riesgos condicionados o validaciones pendientes, no defectos confirmados adicionales. Este dictamen no autoriza integración ni publicación.
