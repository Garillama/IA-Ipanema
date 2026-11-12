## Adenda tras la revisión de Claude del primer candidato

Primer hash revisado: a92a800a51b6611b4362d67012adaad97f9dd50964200ec17102ac510d453bfc, archivado como `../v4-robots-sources-review1.patch`. Claude pidió cambios C1-C3; Codex no completó intervención. Ese ADR no autoriza el candidato nuevo.

Se reprodujeron C1 (comilla abierta dentro del ámbito de otro agente), C2 (namespace/parametro desconocido seguido de noindex) y C3 (lecturas distintas de comas y valores entrecomillados). La revisión 2 mantiene la lectura léxica principal y agrega una lectura alternativa por coma **solo como detector de incertidumbre** dentro de cada fuente física. Si difieren sobre una posible restricción, se registra error/ambigüedad y se devuelve insufficient_evidence, nunca un flag válido proveniente del valor entrecomillado. Una restricción válida de otra fuente sigue prevaleciendo.

Una sintaxis de cabecera con comillas abiertas se trata como incierta incluso dentro de un ámbito no aplicable; no se descarta su posible efecto sobre los límites de ese campo. Esta es una política conservadora del motor. Puede clasificar como desconocidos algunos campos válidos de otros agentes; no se afirma que Google los interprete como globales ni que ignore la restricción.

La ambigüedad entre un prefijo de agente desconocido y un parámetro con dos puntos no se resuelve inventando una lista de bots o concediendo permisos. La lectura alternativa puede inducir unknown, no noindex. La presentación heredada sigue mostrando solo flags comprobados.

Se restauran separadores no alfanuméricos de las acciones que la base excluía (%20, +, ~), sin volver a bloquear la palabra comprar dentro de cualquier texto editorial. En el gate, estados heredados sin evidencia tipada tienen unknown explícito para la comprobación noindex, no un aprobado basado en una subcadena.

La primera pasada de las regresiones generales de la copia aislada detectó que faltaba la fixture KnowledgeTests/Project ipanema; no fue aceptada. Se añadió únicamente un registro sintético y seis índices JSON históricos existentes a la copia temporal, sin credenciales, temas ni nuevo discovery. General unitario posterior: 392 pruebas aprobadas. La suite SEO del estado final de la copia se repitió para conservar hashes de QA coherentes con su configuración sintética.

Hash actual propuesto: 467b97cc915f87ceb289b4aa36b69e8ffc6e2e45749b58b30181a9ad7842b2a9. Evidencia actual en `revision2/validation.json`. 81 específicas incluidas en 165 unitarias SEO, 13 integración, TLS local, suite SEO y 392 unitarias generales aprobadas. El artefacto se aplica directamente a otra copia nueva de los seis módulos base y sus nueve hashes finales coinciden con el árbol probado. No se aplica al workspace. Nueva revisión exacta solicitada; no se trasladan aprobaciones anteriores ni se rebajan controles.
