# Defensa y diseño previo de N2a

Reproducción real local sobre la fixture del candidato fb292ff7: una objeción HIGH se cierra al repetir source:sample.py, sin nuevo hecho ni demostración. Existe confirmación sintética del revisor; no es un bypass del origen. Resultado y condiciones en before-reproduction.json. El estado principal también es approved_for_authorization aunque synthetic_only=true, confirmando el riesgo de lectura parcial N4a.

Causa: add_evidence solo comprueba referencias existentes/probadas; no pide una demostración material ligada a esa objeción. El replay reproduce esa misma condición insuficiente. Acepto N2a. No se requiere novedad textual ni cambiar fuentes: una refutación válida puede demostrar algo no evaluado utilizando los mismos bytes.

Solución mínima: extender la interfaz existente del controlador con una consulta de demostración incremental. Solo acepta un resultado tipado emitido por un verificador confiable después de comprobar hechos o una refutación material. Debe vincular hallazgo, candidato, fuentes, artefacto de demostración y recibo de verificación. No acepta booleanos o hashes del modelo como prueba de materialidad; la comprobación semántica y la procedencia del artefacto son obligaciones del verificador del controlador. Sin implementación real, falla en cerrado. El replay exige además que el recibo de verificación sea vigente, específico y probado; se conserva el reductor único y el revisor originario.

Alternativas rechazadas: pedir un ID/hash diferente (insuficiente); prohibir volver a citar el mismo archivo (rompe refutación documental válida); inventar un evaluador semántico universal o infraestructura nueva (fuera de alcance). Riesgo: el host/controlador sigue siendo frontera de confianza; una clase o hash no autentica un proceso comprometido. La implementación real del verificador debe revisarse por separado.

Fixtures nuevas: verificación determinista de conteos reales en un archivo sintético frente a un hecho/claim original, y pruebas de comportamiento de una función fija del controlador. La misma fuente y el mismo texto pueden aportar refutación material, mientras que un artefacto reetiquetado o con otros hashes pero sin prueba no la aporta. No ejecutar código enviado por modelos.

N4a: nueva versión explícita del resultado con estado synthetic_pass cuando solo pasan fixtures, y authorization_ready=false. El estado operativo aprobado queda reservado para el contrato de procedencia nativa. No cambiar política global ni activar consumidores.

Archivos: code_review.py y test_code_review_v3.py de una nueva copia; council.py permanece idéntico al candidato previo. Preservar N1/N3/N4 y pruebas directamente afectadas. No nuevas llamadas, integración, clientes ni producción. Defensa del autor, no cierre independiente de hallazgos.
