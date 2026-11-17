# A — paquete selectivo de Claude, sin ejecución

Candidato conservado: `69c75ac77596439227c4066439711334e8c7bf2724b5a28fbbfabdf2336e0dbb`. No se modificó el diff ni ninguno de sus tres archivos.

**Entrada preparada: 243,861 bytes**, SHA256 `790b3dcd3e3f40612ff8ddebb45445b23420d13b3864bd28f25b3a35ae1b2060`. Reducción del64.0% frente a677.905bytes. Es el tamaño del archivo preparado, no una nueva medición de envío ni garantía de respuesta.

[Paquete JSON literal](review-packet.json) · [Suficiencia](sufficiency.json) · [Exclusiones y motivos](exclusions.json) · [Análisis del timeout](timeout-analysis.json) · [Handoff no autorizado](execution-handoff-NOT-AUTHORIZED.json).

## Evidencia del timeout

Se reprodujo **exactamente**, sin inferencia, el payload anterior:677.905bytes y hash `5dd778bce7c238524d286869b74f297aa64516399c1ae62865794b5331768f7f`, idéntico al recibo. El revisor no emitió salida antes del watchdog de primera respuesta120s; el límite absoluto era240s. Proceso recuperado. No hay evidencia que permita asignar causa a cuota, autenticación, inicialización del cliente, inferencia o volumen.

El generador `engine.prompt_for`, para el role review, añadía versiones/diffs de adición completa de los archivos de revisión ausentes del commit raíz, mientras esos mismos archivos ya estaban en files. Componentes serializados: review_context≈300,388bytes, files≈290,698, knowledge≈49,651. Los tamaños por componente no se suman como ahorro independiente. **La duplicación del paquete está demostrada; su causalidad en el timeout no.**

## Qué queda

Diff real exacto; manifiesto y hashes; contenido íntegro de los tres candidatos; contratos/schema una sola vez; ocho módulos completos relacionados —incluidos core, adapters, planner, engine, council_runtime, isolation y recovery— y pruebas relevantes de recibos. Las159 pruebas se conservan con su procedencia; no se repitieron.

El baseline council.py omitido no es una dependencia perdida: se verificó que es el prefijo byte a byte idéntico del council.py candidato completo, que aparece una sola vez. Se excluyeron diffs artificiales de los insumos, opiniones previas y conocimiento histórico ajeno a este cambio, no reglas de permisos ni interfaces necesarias.

## Suficiencia y límites

El paquete permite revisar ubicación, reutilización/duplicidad, fronteras de contratos, permisos, identidad, QA y regresiones del cambio acotado. Conserva líneas de archivo y hashes originales. Se verificaron importaciones directas relevantes y se incluyeron módulos completos para evitar perder constantes, callers y supervisor.

No es un certificado de cobertura de todo el repositorio o de capacidad del revisor. Si aparece una dependencia externa al conjunto que resulte material, el revisor debe detener esa conclusión y pedir una expansión exacta al controlador; no adivinar ni iniciar herramientas. No incluye opiniones del autor/pares.

La siguiente llamada **no está ejecutada ni autorizada por esta preparación**. Mantener modelo/perfil y límites120/240 del recibo, sin aumentarlos. Enviar el JSON literal por el transporte existente; no volver a pasarlo sin cambios por el wrapper que generaba diffs de cada insumo. Revisar/autorizar ese handoff antes de la llamada. No se modificó el orquestador para conseguir el recorte.
