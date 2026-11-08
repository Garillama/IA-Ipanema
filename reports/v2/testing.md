# Pruebas y evidencia de V2

Verificación: 2026-11-08T09:13:12.781561+00:00. Entorno Linux, Python 3.12.3, Node 24.22.0, Chrome 155.0.8059.84, Puppeteer 25.16.0, axe 4.14.0, Lighthouse 13.6.0. [Entorno](evidence/environment.json).

| Ejecución | Resultado real | Evidencia |
|---|---|---|
| `qa --suite quick` | 35 unitarias y 7 de integración aprobadas; 10 casos del coordinador aprobados | [QA offline](evidence/qa-offline.json) |
| `qa --suite fixtures` | 7 pruebas de navegador aprobadas, sobre servidor propio de loopback | [QA Chrome](evidence/qa-fixtures.json) |
| `qa --suite source` | 330 archivos, 51 secciones, 54 bloques, 118 snippets; schemas sin errores | [QA de origen](evidence/qa-source.json), [resumen](evidence/source-audit-summary.json) |
| Validación de cierre | Sintaxis, skills, enlaces, conservación del discovery y hashes del tema | [Integridad](evidence/preservation.json) |

Las cifras pertenecen a conjuntos distintos: no son un porcentaje de cobertura del agente o de Ipanema.

## Casos ejecutados

- Portabilidad: entrada original desde otro cwd, copia completa en ruta con espacios, sin tema disponible, configuración incompleta, registro/selección de varias tiendas. Las rutas temporales se crean durante la prueba; no son cinco computadoras diferentes.
- Configuración: prioridades de selección, overrides locales, variable no definida, rutas de evidencia peligrosas, origen distinto, credenciales en configuración/URL y rechazo de red remota sin permiso.
- Corrección controlada: baseline que falla de verdad, primer parche fallido y revertido, segundo parche aprobado y aceptado; preservación de cambios previos, rechazo de conflictos posteriores, archivos nuevos y límite de intentos. No se ejecutó git reset/clean.
- Conocimiento: hero y card nativos, consumidores transitivos, settings, archivo concreto, hallazgos frente a soluciones y configuración desconocida.
- Soluciones: evidencia/hashes obligatorios, IDs sin sobrescritura, invalidación por archivo, prueba o versión observada del tema.
- Navegador: seis anchos (360/390/768/1024/1440/1920), sin JavaScript, reduced motion, axe y teclado del menú en fixture. El control negativo detectó H1 extra, JSON-LD inválido, canonical ausente, enlaces de carrusel inválidos, overflow y fallo de Escape.
- Red: imagen elegida por picture en navegación mobile/desktop, POST bloqueado, 429 que detiene la segunda página y presupuesto de solicitudes excedido de forma deliberada. Se ejecutó el puente Python → Node para página y componente, y el collector histórico de inspección desde otro cwd.
- Rendimiento: Lighthouse real, una muestra local por perfil, con configuración/versión y política de red conservadas. [Mobile](evidence/fixture-samples/lighthouse-mobile.json), [desktop](evidence/fixture-samples/lighthouse-desktop.json). No son resultados de la tienda.
- Comparación: PNG idénticos, píxel cambiado, umbral, máscaras, dimensiones y archivos inválidos; métricas sin contexto o con distinto perfil/configuración son rechazadas, y métricas no medidas no se aprueban.

## Evidencia visual y controles negativos

[Fixture correcto a 390](evidence/fixture-samples/responsive-good-390.png) y [fixture con defectos a 390](evidence/fixture-samples/responsive-broken-390.png). Son controles propios distintos, no un cambio publicado en la tienda. [Fallos detectados](evidence/fixture-samples/negative-control.json).

Una captura fullPage disparó una imagen responsive adicional en el fixture desktop. El registro distingue navigation_network de requests generados durante screenshot/instrumentación; [red y fases](evidence/fixture-samples/desktop-network.json). No se atribuyó esa solicitud a Ipanema ni se infirió descarga por presencia DOM.

La primera protección de red dejaba las pestañas usadas por Lighthouse fuera del interceptor: el servidor local recibió [dos POST sintéticos](evidence/interception-before.json). Se protegieron pestañas iniciales y nuevas, con inicialización compartida; la prueba posterior registró [cero POST en ambos perfiles](evidence/interception-after.json). La suite ahora reproduce ese caso. No hubo solicitudes a la tienda en esta prueba.

La política de lectura puede alterar apps que usan POST y los tiempos observados. Comparar siempre bajo las mismas condiciones y no diagnosticar ese bloqueo como defecto nativo sin otra reproducción autorizada.

## No ejecutado y alcance

No se ejecutó QA nuevo de la tienda real, editor privado, compras/carrito con escritura, checkout, clientes o formularios comerciales. Se conserva la evidencia histórica del discovery por separado. No se ejecutó CI remoto, Windows/macOS físicos, otros navegadores, usuarios reales/INP, Search Console, certificación AA ni un modelo externo implementando A–J. Los scripts históricos específicos de estados/crawl no se reejecutaron íntegramente; se verificaron sintaxis, helpers comunes y un collector real sobre fixtures.

Instalaciones nuevas: ninguna. package.json fija versiones directas observadas, sin lockfile transitivo todavía. Repetibilidad demostrada en este entorno; no se promete reproducción idéntica en cualquier máquina.

Controles de confidencialidad: [escaneo de formatos comunes](evidence/credential-scan.json), validación de configuración y exclusiones Git. El escaneo no equivale a una auditoría exhaustiva de secretos ni sustituye revisar artefactos antes de compartirlos.
