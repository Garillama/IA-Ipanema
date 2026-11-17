# Rhino Performance — decisiones SEO pendientes de evidencia específica

Continuación incremental de [las cinco exportaciones conciliadas](../exports-20261113/README.md), 13 de noviembre de 2026. No se han recibido exportaciones adicionales durante esta intervención. No se han consultado Rhino ni Google, ejecutado rastreos o cambiado archivos de la tienda. Las llamadas a los proveedores del consejo se limitan a revisar los documentos locales; no son consultas a Search Console.

## Decisiones concretas

| Orden | Oportunidad | Evidencia disponible | Decisión actual y siguiente evidencia |
|---|---|---|---|
| 1 | Captar demanda comercial hacia Presoterapia | 2.810 impresiones, 30 clics, CTR exportado 1,07%, posición 5,30 | Priorizar consultas filtradas por URL exacta. Decidir después si existe desajuste de intención/snippet; no modificar título por el CTR agregado. |
| 2 | Entender la visibilidad de Compresión frío/calor | 1.079 impresiones, 6 clics, CTR exportado 0,56%, posición 1,35 | Conservar la página actual y desglosar consultas/segmentos. Esa posición no demuestra que mejorar el título produzca más clics. |
| 3 | Proteger rutas antiguas con tráfico histórico | 94 URLs coinciden exactamente entre ejemplos de redirecciones y rendimiento | Priorizar las cinco de mayor número de clics. No eliminar redirecciones ni asumir destinos por semejanza de slug. |
| 4 | Encontrar exclusiones que afecten a páginas actuales importantes | Resumen: 33 rastreadas sin indexar, 5 descubiertas sin indexar y 33 errores 404 | Esperar sus ejemplos oficiales y conciliarlos por URL exacta. No atribuir esas cantidades a las 124 páginas conocidas. |

Las métricas de las dos categorías corresponden a Web, **11 de agosto–10 de noviembre de 2026**, sin asociación de consulta/país/dispositivo. Las fechas absolutas son el intervalo de las 92 filas diarias de la hoja Gráfico; Filtros declara «Últimos 3 meses», sin fechas absolutas. Confirmar el rango seleccionado antes de comparar nuevas exportaciones. Son una referencia histórica, no una medición de mejoras. El valor comercial potencial es cualitativo: no hay datos de conversiones, ingresos ni ventas por landing que permitan cuantificarlo.

[Backlog detallado](opportunity-backlog.json): hipótesis, evidencia mínima, acción condicional, riesgos y validación por oportunidad. Todas las propuestas de cambios permanecen `needs_evidence`; ninguna está autorizada para implementación.

## Qué podrá decidirse al recibir las consultas

Para cada categoría, identificar primero las consultas reales y separar intención de compra, comparación e información. Conservar el texto original de cada consulta, sus métricas y filtros. La clasificación de intención será una interpretación documentada, no un dato declarado por Google.

Una consulta comercial con desajuste demostrado frente a la landing puede justificar proponer un título o una descripción más precisos. Una consulta informativa no justifica insertar palabras clave comerciales automáticamente. Si los datos respaldan el contenido actual, la decisión válida es conservarlo. No se redactan títulos candidatos todavía.

Las consultas globales como «botas de presoterapia» evidencian demanda en la propiedad, pero aún no pueden asignarse a Presoterapia ni a un producto concreto. Para investigar canibalización se necesita una exportación de Páginas filtrada por esa consulta con periodo y segmentos equivalentes. Que varias URLs aparezcan para una consulta no prueba por sí solo un conflicto: también hay que demostrar competencia de intención o inestabilidad; variantes canónicas y redirecciones se mantienen separadas.

## Redirecciones: evidencia y comprobación mínima propuesta

Búsqueda **offline y limitada** de las cinco URLs prioritarias en 232 archivos JSON/HTML/HAR de familias originales seleccionadas: ninguna coincidencia literal. [Registro reproducible de fuentes, hashes y límites](saved-redirect-evidence-search.json). No se inspeccionaron indiscriminadamente snapshots de trabajadores o todo el historial; por tanto, el resultado significa «sin evidencia localizada en este alcance», no «nunca se comprobaron».

| Ruta histórica | Clics históricos | Impresiones históricas |
|---|---:|---:|
| `/producto/botas-de-presoterapia-botas/` | 539 | 20.338 |
| `/home/` | 283 | 3.519 |
| `/producto/botas-de-presoterapia-kit/` | 100 | 4.973 |
| `/retencion-de-liquidos-en-atletas-por-que-ocurre-y-como-tratarla/` | 76 | 5.504 |
| `/que-debes-saber-antes-de-de-comprar-unas-botas-de-presoterapia/` | 67 | 18.189 |

Los cinco destinos finales, cadenas y correspondencia temática siguen sin comprobar. Estas cifras no representan clics perdidos, valor de conversión ni tráfico actual. No se suman filas de países/dispositivos a estas métricas.

[Alcance propuesto para una autorización posterior](redirect-read-scope.md). No hay manifiesto nuevo autorizado, ejecución ni comando inventado. El mecanismo de selección cerrada existente exige cinco destinos; la combinación de cinco redirecciones probables y tres saltos globales no garantiza completar todas las cadenas. Antes de solicitar ejecución hay que resolver esa compatibilidad sin alterar el motor ni los límites de forma implícita.

## Conciliación de los próximos archivos

[Contrato de entrada](intake-contract.json). Se conservan los archivos originales y hashes, pestaña/fila, motivo literal, fecha de exportación, fecha de actualización disponible y último rastreo como campos distintos. La fecha del nombre del archivo no sustituye la fecha del estado.

- Coincidencia exacta de URL, sin sustituir www, protocolo, barra final o parámetros. Relaciones de variantes se registran aparte y no transfieren estados.
- Si faltan metadatos que demuestren el filtro de página, confirmar el filtro con el propietario antes de vincular consultas a una categoría.
- Conservar observaciones históricas. Un archivo nuevo no elimina estados anteriores; un conflicto se registra y se investiga.
- Ausencia en una tabla de ejemplos no demuestra ausencia de problema, indexación ni cero impresiones. Una tabla de consultas puede ser limitada.
- Separar filtros globales de segmentos. Para México/móvil confirmar el objetivo comercial; no asumir ingresos o ventas por país a partir de clics.
- Impresiones históricas no certifican indexación actual. No construir un total indexado sumando ejemplos parciales e inspecciones.

Se reutilizan [las instrucciones oficiales de exportación ya preparadas](../exports-20261113/next-official-exports.md): listas de rastreadas sin indexar, descubiertas sin indexar, 404 y ejemplos indexados; consultas filtradas por las dos categorías. No hace falta repetir los cinco XLSX ya conciliados.

## Lo que se conserva

124 páginas HTML comprobadas individualmente, 122 caminos HTML observados, 14 productos, cinco categorías y 86 artículos. Quince inspecciones históricas con diez URLs conocidas como indexadas no representan el total del dominio. Se conservan las advertencias de datos estructurados, los 20 artículos con campos incompletos y el canonical paginado del blog sin nuevos cambios o consultas. No se desbloquean rutas de checkout o add-to-cart: sus exclusiones son un asunto distinto de las páginas comerciales candidatas a indexación.

## Revisión y controles

[Revisión incremental real completada](review-status.json): ambos proveedores entregaron contratos válidos y respondieron las dos preguntas cruzadas. Se resolvieron tres precisiones documentales; permanece pendiente la viabilidad del alcance de redirecciones (`codex-obj-02`), además de la evidencia operativa de cada oportunidad. [ADR incremental](ADR.json). No sustituye los consejos anteriores, no habilita implementación y no simula aprobaciones. Los hashes de las matrices y del ADR anterior están en [protected-baseline-hashes.json](protected-baseline-hashes.json).


## Resultado y siguiente paso

Prioridad acordada para investigar: **Presoterapia**, seguida de Compresión frío/calor. No hay una corrección de contenido o técnica demostrada por estas nuevas comprobaciones offline. El paquete está preparado para conciliar los archivos pendientes sin repetir auditorías. La revisión documental está terminada; las propuestas de intervención siguen `needs_evidence`, con `implementation_allowed=false`.

Al aportar los nuevos archivos, se podrá identificar qué consultas corresponden a cada landing, qué exclusiones afectan exactamente al inventario y cuál es la primera modificación justificable. No hace falta autorizar publicación o rastreo para importar exportaciones oficiales locales.
