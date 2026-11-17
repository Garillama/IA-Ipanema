# ADR — revisión cruzada contextual ligada al diff

Estado: **needs_evidence**. `implementation_allowed:false`. Solo candidato aislado; integración y activación no autorizadas por una revisión completa.

Decisión propuesta: extender `council.py` con un punto de entrada opcional y un helper de contratos/gates sin inferencia. Reutilizar validador, ledger y guardas de rutas existentes. Un autor efectivo, dos revisores de proveedores distintos y cinco challenges; HIGH/BLOCKER abiertos impiden aprobación. Las correcciones invalidan revisiones previas.

Alternativas rechazadas: reglas solo en prompts; otro orquestador; reutilizar detectores de duplicidad SEO para código; cambiar el agregado dual actual; habilitar Antigravity o CommandCode sin transporte seguro.

Investigación de fuente y ubicación: design-packet.json y README.md. No se declara aprobado el preconsejo: Claude quedó rate_limit, Codex emitió una propuesta recuperada del mismo recibo y Antigravity no fue invocado. No hay contraste/defensa ni revisión final independiente de los dos proveedores requeridos.

Resultados del controlador:31 pruebas nuevas y128 existentes aprobadas en copia privada de herramientas. Las identidades/revisiones de las unitarias son sintéticas. No demuestran detección semántica real ni ejecución autenticada de Antigravity.

Pendientes obligatorios: revisión real Claude+Antigravity del diff final, aceptación contextual sobre fixtures ocultando respuestas esperadas, validación del almacén de recibos/identidades al conectar el engine y habilitación segura del adaptador V3 en lote separado. No reemplazar evidencia por votos.

Parche candidato:69c75ac77596439227c4066439711334e8c7bf2724b5a28fbbfabdf2336e0dbb. Tres archivos,1modificación y2altas, sin eliminaciones. Hashes y backup en candidate-manifest.json y recibos del controlador. No se modificaron fuentes operativas, modelos, políticas o proyectos de clientes.

Un futuro `approved_for_authorization` del helper no habilita integración/publicación. El controlador conserva permisos, estado, QA y decisión operacional; el propietario conserva autorización específica para efectos remotos. No hay cambios de producción ni reversión ejecutada.
