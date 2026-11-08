# Comprobación antes de entregar un cambio

Aplicar lo relevante al cambio; una edición reversible de espaciado no exige una batería de pruebas comerciales.

- Identidad de tienda, instalación, versión, fork y fuente del componente comprobadas.
- Funcionalidad nativa y consumidores revisados; sin motor, helper o regla de negocio duplicados.
- HTML inicial conserva contenido, enlaces, semántica y dimensiones; layout correcto antes de JS.
- CSS modifica la fuente/variante adecuada, con selector acotado y sin escalada innecesaria de especificidad.
- Desktop/mobile usan un solo contenido; revisar 768 y 1024 además de extremos.
- currentSrc, sizes, DPR, prioridad y solicitudes ocultas revisados para cambios de imágenes.
- Interacción no añade tareas largas, timers/listeners repetidos ni trabajo de layout evitable.
- Movimiento respeta reduce y permite usar/leer el contenido.
- Teclado/foco/nombres y estados pertinentes comprobados.
- Metadatos/JSON-LD no duplicados y contenido de producto veraz.
- Comparación antes/después usa misma ruta/datos/perfil; números propuestos separados de resultados.
- Diff incluye eliminaciones y preserva cambios del comerciante; publicación dentro de autorización aplicable.
- Entrega explica resultado, reutilización, pruebas reales y límites; actualiza la fuente principal del conocimiento.

Fuentes de verificación: [matriz QA](../10-quality/testing-matrix.md), [presupuestos](../05-performance/performance-budgets.md), [riesgos](../10-quality/regression-risks.md).
