# Paginación: controles para la operación exacta

## Alcance y condiciones previas

Instalación publicada 14828608, tienda 7400935. Solo los dos archivos del manifest. No incluye menú, footer, blog, canonicals, aplicaciones ni catálogo. No se cambia a paginación clásica ni se reemplaza LS.

El diff conserva la configuración de carga infinita. Añade una fila visible con enlaces anteriores/siguientes independientes, numerados cuando la plataforma proporciona una página numérica válida. Reutiliza estilos existentes; no promete una apariencia idéntica. La navegación se nombra «Página: productos». Tras anexar productos, el enlace sigue representando una página independiente, no la siguiente tanda acumulada por JavaScript.

Con JavaScript, el botón se habilita tras inicializar LS.hybridScroll; la carga sigue a cargo del controlador nativo. Al activarlo con teclado se conserva un foco estable durante la espera y se dirige al primer producto nuevo solo si el usuario no movió el foco. Con puntero no se impone foco. Sin JavaScript el botón queda visible/deshabilitado y los enlaces separados permiten navegar. La aceptación del propietario debe incluir estas diferencias visibles.

Antes de una ejecución autorizada: comprobar otra vez instalación productiva, hashes before de ambos archivos y hash del parche; verificar respaldo de bytes contra esos hashes y ausencia de sincronizadores activos. Detener ante cambios concurrentes. Confirmar que baseline y contenido siguen vigentes; refrescar solo si existe deriva relevante. Exigir revisión independiente final y autorización específica del propietario. Ningún reporte del modelo concede permisos.

La CLI instalada no ofrece `--file` en theme push. No usar `--force`, watch ni theme publish. La futura operación debe emplear el guard existente de transporte, ligado a tienda, instalación, lista de dos rutas y hashes after; comprobar antes del envío que el diff efectivo contiene exactamente esas dos modificaciones y cero eliminaciones. Preparar una vista de lectura temporal del candidato, sin copiar credenciales ni cambiar otros archivos. Si no puede demostrarse ese alcance, detener; no subir el árbol completo. Este documento no ejecuta comandos de publicación.

## QA inmediato posterior — todo pendiente hasta autorización y despliegue

1. **Integridad:** GET de los dos archivos y comparación con hashes after; confirmar que solo cambió el alcance aprobado. Conservar fecha y respuestas saneadas. Detener nuevos cambios si falta un archivo o un hash difiere.
2. **HTML inicial:** `/productos/` y `/productos/page/2/`: HTTP 200, canonical propio conservado, title/H1/robots/JSON-LD sin regresiones; enlaces reales a página 2 y retorno cuando corresponda. No afirmar indexación por esta prueba. Registrar controles y valores Twig renderizados reales.
3. **Carga nativa:** con LS publicado, verificar secuencia real de 12 a 14 productos, unicidad de IDs, orden y enlaces de tarjetas, estado final del botón/spinner. No inventar página 3: no existe evidencia de ella en el catálogo actual. No automatizar compra ni envío de formularios.
4. **Sin JavaScript:** comprobar contenido y enlaces desde HTML, botón deshabilitado, navegación al destino independiente. No presentar una inyección DOM como HTML inicial.
5. **Teclado/AX:** Tab, Enter y Espacio; nombres de botón y navegación; foco durante espera, éxito y movimiento voluntario del usuario; ausencia de foco perdido o robado. El caso de fallo de red se puede reproducir en el navegador con intercepción local explícita; no provocar errores del servidor. Conservar la distinción entre datos reales y fixtures.
6. **Responsive/visual:** 360, 390, 768, 1024, 1440 y 1920 px; capturas antes/después, fila numerada esperada, sin recorte, desbordamiento ni controles inaccesibles. No cambiar tipografía ni diseño para lograr el test. Comparar el mismo estado de scroll y contenido; máscaras explícitas solo para contenido dinámico ajeno.
7. **Filtros/orden y consumidores:** en la configuración actual no están expuestos; registrar no aplicable, no inventar parámetros. Si aparecen habilitados al publicar, detener aceptación hasta probar conservación de parámetros/IDs. Revisar consola, slider de tarjetas y smoke de home, PDP y blog porque store.js es compartido; sin operaciones comerciales. No atribuir incidencias previas del footer a esta modificación.
8. **Rendimiento:** repetir cinco muestras por dispositivo de `/productos/` con el mismo protocolo del baseline. Mantener URL final, Chrome/Lighthouse, viewport, CPU, red, caché, consentimiento y política de recursos. Conservar cada muestra y métricas correlacionadas; mediana, rango y variabilidad. Comparar transferencia/JS/CSS/imágenes/solicitudes disponibles, LCP/FCP/CLS/TBT/Speed Index y scores. No inferir INP de TBT ni mezclar con PageSpeed/CrUX.

## Decisión del controlador

Fallo funcional, pérdida de enlaces/canonical, duplicados, error nuevo de JS o regresión de foco: rechazar aceptación. No esperar una puntuación para detectar un fallo crítico.

Para laboratorio, reutilizar los comparadores existentes con perfiles equivalentes. Predeclarar alertas: caída de mediana de score >=5 puntos; aumento de mediana de LCP/FCP/Speed Index >10% y >200 ms; TBT >20% y >100 ms; CLS +0,02; transferencias/solicitudes adicionales no explicadas por los dos archivos. Son umbrales operativos de investigación, no significancia estadística garantizada con cinco muestras. Examinar dispersión/MAD e incidencias externas; una única muestra o fluctuación dentro del ruido no confirma regresión. Si faltan perfiles comparables o hay solapamiento/ruido que impide decidir: `inconclusive` o `insufficient_evidence`, no aprobado. Una regresión confirmada bloquea aceptación. No se promete 90+ por este cambio SEO.

## Reversión exclusiva, condicionada a autorización

Solicitar que la autorización incluya restaurar únicamente estos dos archivos si falla el QA. Antes de revertir, volver a leer ambos y exigir los hashes after aprobados. Restaurar los bytes de `remote-before` indicados en manifest, comprobados contra los hashes before. Cualquier cambio posterior ajeno, identidad dudosa o estado parcial diferente obliga a detenerse y solicitar decisión; no sobrescribirlo.

Después: comprobar hashes before publicados, repetir HTML/enlaces/carga nativa/teclado y registrar el incidente. No restaurar toda la tienda ni el árbol de trabajo. No tocar el menú o canonicals. Sin autorización de reversión, detener y presentar el incidente, no ejecutar una escritura remota por iniciativa propia.
