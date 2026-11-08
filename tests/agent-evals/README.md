# Evaluación del agente

[cases.json](cases.json) contiene diez tareas A–J: reutilización del hero, SEO de carrusel, imágenes/red, responsive, card compartida, H1/contenido, carrito, motion, producción no autorizada y conocimiento desconocido.

`python3 tools/ia.py evals` ejecuta el coordinador real contra la base existente. Comprueba capacidades seleccionadas, componente nativo correcto cuando corresponde, consumidores, existencia de referencias, fecha, controles de permiso y pruebas previstas. Registra tiempo de la herramienta y bytes de evidencia recuperada. Esas medidas no son tokens/contexto de un modelo ni tiempo total de una implementación.

El score del coordinador no acredita que la IA haya generado una implementación correcta. No se llama a APIs de inferencia, no se envía código del comerciante y no se estima un coste sin datos.

## Ejecución externa por versión

Abre una copia aislada del repositorio con el runtime/modelo a evaluar. Ejecuta los prompts sin mostrarle la respuesta esperada, dentro de un tema de pruebas autorizado o fixtures propios. Conserva versión/modelo, hash de instrucciones, tiempos/usage reales si el runtime los expone, decisiones observables, diff, QA y capturas. No hay obligación de ejecutar subagentes; este repositorio no supone que el runtime los soporte.

El evaluador prepara JSONL con un objeto por caso:

```json
{"case":"A","decision":"reuse_native","references":["ipanema-discovery/02-native-components/specifications/sections--hero.md"],"qa_reports":["reports/runs/proyecto/ejecucion/report.json"],"manual_interventions":0,"measured_tokens":null,"measured_cost":null}
```

Las decisiones esperadas están en cases.json, para el evaluador. `evals --responses ARCHIVO` valida referencias, existencia de pruebas QA aprobadas y decisión declarada. No prueba que la narración sea cierta ni sustituye revisar el diff. Respuestas faltantes quedan no ejecutadas; respuestas erróneas hacen fallar la evaluación de artefactos. El consumo/coste proporcionado se etiqueta como medición aportada, no medida por el CLI.

La revisión funcional/visual debe calificar: cumplimiento, calidad de decisión, reutilización, regresiones y seguridad. Adjunta evidencia que cubra el caso, no un QA genérico. Las tareas que requieren estado comercial, producción, un modelo externo o una tienda inaccesible quedan pendientes, sin inventar aprobaciones.

[Resultados de esta migración](../../reports/v2/evaluation.md).
