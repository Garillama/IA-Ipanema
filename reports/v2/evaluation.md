# Evaluación de IA-Ipanema V2

Estado: **10/10 casos del coordinador aprobados; evaluación integral de un modelo externo no ejecutada**. [Resultado reproducible por versión](evidence/coordinator-evaluation.json), [casos y protocolo](../../tests/agent-evals/README.md).

Se ejecuta el código real de planificación/recuperación sobre el inventario, grafo y documentos existentes. Se verifica selección de capacidades, candidato nativo donde corresponde, consumidores, existencia de referencias, fechas, permisos y pruebas previstas. No se simula una respuesta de un modelo ni se afirma que implementó diez cambios.

| Caso | Tarea | Coordinador | Tiempo de herramienta (s) | Bytes recuperados |
|---|---|---|---:|---:|
| A | Hero nativo | passed | 0.203 | 19484 |
| B | Carrusel rastreable | passed | 0.443 | 15395 |
| C | Imágenes y red | passed | 0.381 | 23469 |
| D | Layouts por dispositivo | passed | 0.213 | 15320 |
| E | Card compartida y consumidores | passed | 0.399 | 11936 |
| F | H1 de tema o contenido | passed | 0.418 | 12200 |
| G | Carrito y contratos | passed | 0.340 | 10282 |
| H | Motion y rendimiento | passed | 0.243 | 3806 |
| I | Producción sin autorización | passed | 0.459 | 10959 |
| J | Configuración desconocida | passed | 0.071 | 580 |

El tiempo mide la herramienta de planificación; los bytes son el JSON recuperado antes de cargarlo al modelo. Tokens, coste de inferencia, calidad funcional de una implementación y regresiones de tienda: **no medidos**. El detalle de capacidades y checks está en el JSON. Las acciones de producción no se ejecutaron; se probó su denegación en el contrato de permisos.

El evaluador externo acepta JSONL, valida referencias y pruebas y conserva casos faltantes como no ejecutados. Calidad de decisión/UX, fidelidad al pedido y pertinencia de pruebas necesitan revisar una ejecución real. El repositorio no instala ni llama automáticamente otro modelo, ni presupone agentes paralelos.

## Correcciones aprendidas durante la migración

[Primera evaluación](evidence/coordinator-initial-failure.json): palabras genéricas desplazaban al hero y producían resultados ante un identificador desconocido. Se corrigieron ranking/normalización, se añadieron controles de regresión y se comprobó la referencia real. El caso A también tenía una expectativa inicial equivocada (`blocks/hero.tpl`); se corrigió a `sections/hero.tpl` después de consultar el inventario y la fuente. No se creó ese archivo supuesto.

La comprobación de configuración desconocida ahora devuelve ausencia de candidatos; no convierte documentación inexistente en una capacidad. Las pruebas de artefactos no constituyen una auditoría completa de exactitud semántica del modelo.

Próxima evaluación: ejecutar A–J a ciegas en una copia aislada con runtime/modelo identificado y tema de pruebas autorizado; conservar diff, QA, uso real si está disponible y revisión independiente. Ningún resultado de esa fase se da por aprobado aquí.

## Protocolo del evaluador externo

Se ejecutaron además tres controles sintéticos del receptor: artefactos formalmente válidos → passed, casos faltantes → partial y referencia/decisión inválida → failed. [Entradas y resultados reproducibles](evidence/evaluator-controls/results.json). No son respuestas de un modelo; muestran que el receptor distingue esos estados. La pertinencia funcional de un QA válido sigue requiriendo revisión.
