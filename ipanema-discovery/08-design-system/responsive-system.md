# Sistema responsive reutilizable

Fecha: 2026-11-08. Fuente principal para cortes y controles: [responsive del editor](../03-editor/responsive-controls.md).

La arquitectura propuesta mantiene un árbol de contenido por componente, base mobile y reglas de composición por breakpoint. Identidad compartida en tokens, diferencias de layout en el componente y contenido/configuración en JSON de instancia. No duplicar el HTML completo de desktop para esconderlo en mobile.

Si un control mobile ya existe, usarlo. Si no existe y el diseño lo necesita, evaluar un setting acotado o una variante CSS; no crear dos secciones con copias del mismo catálogo. Evitar IDs de breakpoint que nadie pueda ajustar consistentemente o campos de padding por lado sin caso de uso.

El tamaño tablet debe validarse explícitamente: el corte de 768 activa contratos desktop antes de llegar a un portátil. El desborde observado en home y una PDP a 768/1024 demuestra que una buena captura a 390 y 1440 no basta. No solucionar con overflow-x hidden en body sin localizar al responsable: puede ocultar navegación y foco.

Las pruebas incluyen contenido largo, zoom/reflow, cambios de orientación y secuencia de resize; la inicialización JS según innerWidth puede dejar estados antiguos tras cruzar el corte. Un media query correcto no garantiza que el motor interactivo se destruya/reinicie correctamente.
