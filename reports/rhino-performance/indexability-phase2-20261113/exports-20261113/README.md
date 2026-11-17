# Rhino Performance — conciliación de exportaciones oficiales de Google

Archivos recibidos13 noviembre2026. **Se importaron los cinco XLSX sin instalar dependencias, ejecutar fórmulas o modificar los originales.** No se consultó el storefront, Search Console API ni OAuth. La conciliación es offline y conserva el baseline124/124 HTTP,122 rutasHTML y15 inspeccioneshistóricas.

## Resultado principal

El último punto del gráfico de cobertura, **8 noviembre2026**, muestra **141 URLs indexadas y347 sin indexar** en «Todas las páginas conocidas». Son cifras de la propiedad exportada, no el resultado de clasificar nuestras124 HTML. El archivo no trae la lista de las141.

La tabla de motivos indica:

| Motivo literal de Google | Recuento exportado | Detalle recibido |
|---|---:|---|
| Página alternativa con etiqueta canónica adecuada | 148 | 148 ejemplos |
| Página con redirección | 112 | 112 ejemplos |
| No se ha encontrado(404) | 33 | Solo total |
| Bloqueada por robots.txt | 16 | 16 ejemplos |
| Rastreada: actualmente sin indexar | 33 | Solo total |
| Descubierta: actualmente sin indexar | 5 | Solo total |
| Soft404 | 0 | Sin URLs positivas aportadas |
| Excluida por noindex | 0 | Sin URLs positivas aportadas |
| Duplicada: canonical elegido diferente al del usuario | 0 | Sin URLs positivas aportadas |

Las razones suman347, pero el nombre de hoja «Problemas críticos» **no convierte alternativas, redirecciones y bloqueos comerciales esperados en defectos a corregir**. Los ejemplos pueden ser limitados. Fecha del archivo, último punto del gráfico y último rastreo de cadaURL son campos separados: algunos rastreos llegan al10 noviembre. No se imputa el8 o13 noviembre como fecha precisa del estado de cadaURL.

[Resumen](summary.json) · [Cobertura agregada y motivos originales](coverage-aggregate.json) · [fuentes ySHA256](source-manifest.json).

## Matriz de124: sin transferir estados entre variantes

Las tres tablas entregadas contienen276 filas:148 alternativas,112 redirecciones y16 robots. **Cero filas coinciden exactamente con unaURL de la matriz124**. Por ello no se asignó a ninguna de esas124 una nueva exclusión a partir de otra variante.

Se conservan113 relaciones candidatas en alternativas y2 en redirecciones por path equivalente, diferencias dehost/esquema/barrafinal, conqueryidéntica. Son filas relacionadas, no113 páginas distintas ni destinos canonical demostrados. UnaURL sinbarra o conwww puede ser alternativa de una limpia, pero el archivo **no dice cuál es su canonical elegido**. No se certifica esa relación ni se transfieren estados.

[Matriz conciliadaCSV](url-matrix-124.csv) · [JSON](url-matrix-124.json) · [276observaciones oficiales confecha/fuente/fila](official-excluded-URL-observations.json).

La evidencia URLInspection previa sigue siendo10 PASS históricos,1 descubierta sin indexar y4 URLs desconocidas porGoogle en aquellas fechas. Las109 sin inspección siguen sin ese resultado individual. Ahora conocemos además el agregado141 y la visibilidad histórica de108 URLs exactas del inventario en la tabla de rendimiento; **ni141 ni108 sustituyen el estado individual de las124**.

Los resultados originales no fueron sobrescritos: cada fila conserva los campos de inspección histórica, observaciones exactas de las exportaciones, variantes relacionadas y métricas de periodo en columnas separadas.

## Bloqueosrobots: no desbloquear la compra

Las16 URLs son1 checkout y15 rutas con`add-to-cart`. Ninguna es unaURL exacta del inventarioHTML conocido. No se visitaron y no se propone desbloquearlas ni convertirlas en candidatasSEO. Su presencia en el informe no demuestra queGoogle tenga bloqueadas las categorías o productos limpios.

[Observaciones completas](official-excluded-URL-observations.json). Cualquier cambio futuro de reglas exigiría comprobar el recurso concreto, su intención y permisos, no bajar artificialmente el conteo del informe.

## Redirecciones con visibilidad histórica: prioridad de conciliación

Hay94 coincidencias exactas entre ejemplos de redirección y filas del periodo de rendimiento. No significa que las112 tengan tráfico ni que la redirección esté mal. Las rutas con más clics históricos merecen identificar y contrastar su destino **antes** de proponer corrección:

| URL exportada | Clics históricos | Impresiones históricas | Estado de investigación |
|---|---:|---:|---|
| [https://rhino-performance.com/producto/botas-de-presoterapia-botas/](https://rhino-performance.com/producto/botas-de-presoterapia-botas/) | 539 | 20338 | Destino no incluido en exportación |
| [https://rhino-performance.com/home/](https://rhino-performance.com/home/) | 283 | 3519 | Destino no incluido en exportación |
| [https://rhino-performance.com/producto/botas-de-presoterapia-kit/](https://rhino-performance.com/producto/botas-de-presoterapia-kit/) | 100 | 4973 | Destino no incluido en exportación |
| [https://rhino-performance.com/retencion-de-liquidos-en-atletas-por-que-ocurre-y-como-tratarla/](https://rhino-performance.com/retencion-de-liquidos-en-atletas-por-que-ocurre-y-como-tratarla/) | 76 | 5504 | Destino no incluido en exportación |
| [https://rhino-performance.com/que-debes-saber-antes-de-de-comprar-unas-botas-de-presoterapia/](https://rhino-performance.com/que-debes-saber-antes-de-de-comprar-unas-botas-de-presoterapia/) | 67 | 18189 | Destino no incluido en exportación |

[94cruces exactos conservados](legacy-redirect-visibility.json). No tenemos suscabecerasLocation, cadena, destinoactual o relevancia del destino en estos archivos. No se afirma migración desde una plataforma concreta, pérdida de tráfico, redirectdefectuoso o necesidad de sustituirlo. La visibilidad está acumulada en fechas distintas del diagnóstico de exclusión; pueden coexistir sin contradicción.

Primero revisar documentación ya guardada; si se necesita una lectura real nueva, preparar un alcance mínimo de rutas públicas y solicitar autorización separada. No se ejecutó ninguna lectura de esasURLs.

## Rendimiento: periodo y dimensiones reales

Filtros recibidos: Web(basada en texto), «Últimos3 meses». Fechas de las92 filas diarias: **11 agosto–10 noviembre2026**. No se compara ese periodo directamente con la muestra anterior12 octubre–8 noviembre para declarar crecimiento atribuible a cambios.

El archivo contiene440 filas de páginas,1000 consultas,161 países,3 dispositivos y2 apariencias. Las tablas son **marginales separadas**, no consulta×página×país×dispositivo. Tener una fila de «botas de presoterapia» y otra de`/presoterapia/` no demuestra su asociación.

| Tabla | Clics sumados | Impresiones sumadas | Uso correcto |
|---|---:|---:|---|
| Gráfico diario | 5431 | 212491 | Total de su propia serie |
| Páginas | 5577 | 259926 | Agregación de sus440 filas |
| Consultas | 2811 | 71722 | Solo1000 consultas exportadas |

Las diferencias están observadas, pero su causa concreta no queda demostrada por estos archivos. No se fuerza la coincidencia, no se rellenan consultas faltantes y no se suman las dimensiones. LosCTR y posiciones deGoogle se mantienen tal como fueron exportados, con su redondeo; no se calcula una posición global promediando promedios. [Alcance y totales](performance-scope.json).

Móviles:4345 clics/178377 impresiones; Ordenador:1030/32772; Tablet:56/1342. Son datos globales; no se atribuyen a una categoría concreta. México presenta4191 clics en su tabla: es razón para estudiar ese segmento, no prueba de conversiones ni del único mercado servido.

## Cinco categorías comerciales

| Categoría exacta | Clics | Impresiones | CTR exportado | Posición media exportada |
|---|---:|---:|---:|---:|
| [https://rhino-performance.com/presoterapia/](https://rhino-performance.com/presoterapia/) | 30 | 2810 | 1.07% | 5.30 |
| [https://rhino-performance.com/pistolas-de-masaje/](https://rhino-performance.com/pistolas-de-masaje/) | 0 | 45 | 0.00% | 6.78 |
| [https://rhino-performance.com/terapia-fria/](https://rhino-performance.com/terapia-fria/) | No devuelto | No devuelto | Desconocido | Desconocido |
| [https://rhino-performance.com/compresion-frio-y-calor/](https://rhino-performance.com/compresion-frio-y-calor/) | 6 | 1079 | 0.56% | 1.35 |
| [https://rhino-performance.com/accesorios/](https://rhino-performance.com/accesorios/) | 27 | 1071 | 2.52% | 3.49 |

[Datos por categoría](categories.json). No hay fila exacta de Terapiafría: no significa cero tráfico o noindexación. Presoterapia yAccesorios conservanPASS de inspección del12 noviembre; las otras tres categorías no tienen una inspección individual aportada. Las cinco tienenHTTP y caminosHTML válidos en el baseline.

**Prioridad comercial basada en evidencia:** Presoterapia tiene2810 impresiones y30 clics; Compresión frío/calor1079 y6. Ambas justifican obtener la relación consulta-página y sus segmentos. La posición1,35 deCompresión yCTR0,56% **no prueban por sí solos un problema de título, contenido o indexación**. Tampoco45 impresiones dePistolas permiten prometer un beneficio grande.

No se cambiaron títulos, descripciones o contenido. La siguiente propuesta editorial requiere consultas por página, intención, dispositivo/país y evidencia comercial antes de escoger qué modificar.

## Consultas candidatas, aún sin landing atribuida

| Consulta | Clics | Impresiones | CTR exportado | Posición media |
|---|---:|---:|---:|---:|
| botas de presoterapia | 47 | 7396 | 0.64% | 7.79 |
| botas presoterapia | 44 | 7346 | 0.60% | 10.02 |
| botas de compresion | 41 | 5905 | 0.69% | 6.53 |
| pistola de percusion | 10 | 1185 | 0.84% | 9.02 |
| para que sirven las botas de compresion | 1 | 1018 | 0.10% | 7.91 |
| botas compresion | 8 | 985 | 0.81% | 7.86 |
| botas de compresión | 2 | 768 | 0.26% | 9.93 |
| recuperación deportiva | 2 | 752 | 0.27% | 13.43 |

[30candidatas y su clasificación provisional](query-opportunities-candidates.json). El filtrado excluye formasrhino/rino como selección práctica, no clasificación exhaustiva de marcas o intención. La intención comercial/informativa es una hipótesis lingüística; no se inspeccionó laSERP ni se confirmó la página receptora. No se agrupan consultas sumando impresiones como si fueran usuarios únicos ni se asignan automáticamente a categorías.

## Acciones que sí tienen fundamento ahora

| Prioridad | Acción | Evidencia y límite | Riesgo / permiso |
|---|---|---|---|
| P1 | Obtener listas de33 rastreada sin indexar,5 descubierta y33 errores404 | Los totales existen; faltanURLs para conciliación | Lectura deexportación; sin producción |
| P1 | Obtener ejemplos indexados |141 es agregado, no identificación de las124 | No prometer censo completo |
| P1 | Consultas filtradas porPresoterapia yCompresión, con segmentos comparables | Datos actuales de páginas yconsultas separados | No reescritura hasta confirmar relación |
| P1 | Conciliar destinos de rutas históricas con mayor exposición |94 cruces exactos; destino y fallo desconocidos | NuevosGET o cambios requieren permiso separado |
| P2 | Conservar alternativas y bloqueos de operaciones comerciales |0 coincidencias exactas coninventario;16 robots sensibles | No quitarcanonicals o robots para silenciarconteos |
| P2 | Mantener condiciones previas de20 artículos,author/Product yblog | Exportaciones no aportan headers/main,autoría ni mecanismoTiendanube | No reabrir ni cerrar estados artificialmente |

[Backlog conimpacto,risk yautorización](prioritized-actions.json) · [Exportaciones concretas acontinuación](next-official-exports.md).

No se ha demostrado un nuevoP0 sobre las124 URLs limpias. La ausencia de detalle de404/rastreada/descubierta **no demuestra que no haya problemas importantes fuera de la muestra recibida**.

## Revisión incremental Claude + Codex

Se completaron dos revisiones iniciales independientes, contraste y respuestas, más una aclaración semántica acotada de Claude: su primera fila de respuesta trató redirecciones en lugar de la pregunta asignada de categorías. Se conserva sin reemplazar y la aclaración responde la pregunta correcta. No se considera respondida solo porque elJSON fuese válido.

| Agente | Etapa | Modelo / esfuerzo | Duración | Recibo |
|---|---|---|---:|---|
| claude | review | claude-sonnet-5-5 / medium | 34.95s | [claude-review.json](claude-review.json) |
| codex | review | gpt-6.1-sol / medium | 39.27s | [codex-review.json](codex-review.json) |
| claude | contrast | claude-sonnet-5-5 / medium | 35.82s | [claude-contrast.json](claude-contrast.json) |
| codex | contrast | gpt-6.1-sol / medium | 50.00s | [codex-contrast.json](codex-contrast.json) |
| claude | clarification | claude-sonnet-5-5 / medium | 16.35s | [claude-clarification.json](claude-clarification.json) |

[ADR incremental](ADR.json) · [revisión final del controlador](controller-final-review.json) · [métricas declaradas por runtimes](council-runtime-metrics.json). Ambos proveedores favorecen obtener evidencia antes de cambios; Claude conserva changes_requested y Codex proposed. ElADR permanece **needs_evidence**, sin aprobación de implementación. Las preguntas verificaron límites de prioridad de redirecciones y porqué elpromedio deCompresión no prueba defecto decontenido.

 No se reabre el consejo del motor. `implementation_allowed` permanecefalso: los archivos no autorizan cambiar la tienda ni arreglarun estado agregado. Las causas de la diferencia de totales, eljoin consulta-página y los destinos de redirección siguen desconocidos hasta su evidencia.

## Integridad y seguridad

Originales leídos porZIP/XML, sin guardar modificaciones, ejecutar fórmulas o instalaropenpyxl. Los números de fechaExcel se convierten usando la época1900 verificada enworkbook; se conserva elserial original junto con lafecha. No se consideró la fecha delnombre como actualización exacta de cada estado. El propioXLSX no identifica lapropiedad enmetadatos: la atribución proviene del usuario/nombres y de comprobar que todas lasURL corresponden aldominioRhino y varianteshttp/www.

Los valoresGoogle nuevos se incorporan en una **proyección de conciliación**, sin sustituir los históricos o el baseline técnico. Los cincoSHA originales y los artefactos finales quedan sellados. No hubo solicitudes alstorefront,cuentaGoogle, nuevasautenticaciones, rastreos, QA anterior, publicaciones ni modificaciones del motor, tema, menús, catálogo, artículos o canonicals.

[Verificación de integridad](verification.json) · [Sellos de artefactos](artifact-hashes.json).
