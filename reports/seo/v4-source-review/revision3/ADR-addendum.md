# Adenda final del candidato — revisión 3

Candidato sin aplicar. Hash: 7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0.

Se mantiene el aislamiento de cada meta/cabecera y la agregación tipada. Las restricciones válidas permanecen monotónicas. La detección alternativa nunca genera flags válidos: solo incertidumbre.

## Respuestas a la revisión del hash 467b97cc…

- Gate: un noindex válido posterior no queda oculto por unknown del baseline. Se bloquea la aceptación; dos reportes heredados sin evidencia siguen unknown. No se inventa un estado de indexación a partir de una cadena heredada.
- Ámbito válido de otro agente: se conserva entre comas cuando el prefijo y la primera regla forman una lista reconocida, por ejemplo otherbot: nofollow, noindex. Un namespace/parametro ambiguo con una primera regla no interpretable, como max_snippet: -1, noindex, sigue unknown. No se usa una lista arbitraria de nombres de bots para lograr un aprobado.
- Gramática citada: un parámetro desconocido que lleva separadores dentro de comillas se marca incierto, también con punto y coma/espacios. Sus palabras no se convierten en flags. La prueba anterior que esperaba candidato para un valor opaco con un separador se fortaleció a unknown, conservando un assert separado noindex=False.
- User-agent de robots.txt: se conservan errores bloqueantes si una sintaxis inválida puede afectar a Googlebot, al agente propio o a wildcard. Los agentes inválidos ajenos como MJ12bot/360Spider/Sogou web spider generan warnings y no borran reglas parseables de los grupos válidos. No se relaja el caso Googlebot/2.1: permanece unknown/bloqueado conservadoramente, documentado como límite de compatibilidad. Se exportan errores/warnings en la evidencia de robots del crawler.
- Se mantienen las correcciones de separadores de acciones, controles DNS/TLS/redirecciones y presupuestos. El tema y la red no se tocan.

85 específicas incluidas en 169 unitarias SEO; 13 integración, TLS real local, suite SEO y 396 unitarias generales aprobadas. Los nueve archivos del artefacto aplicado a otra copia nueva coinciden con los hashes del árbol probado. La prueba original de fuentes y todos los contraejemplos posteriores se conservan antes/después, incluidos intentos no aceptados. No se aplica al workspace.

Las reglas de incertidumbre son conservadoras del motor y pueden reducir candidatos ante extensiones no soportadas; no se presentan como comportamiento observado de Google. La documentación oficial no define una recuperación exhaustiva de parámetros malformados. No se baja el consejo ni se trata un reporte del autor como aprobación independiente. Se solicita revisión nueva del diff completo; ninguna aprobación de hashes anteriores se transfiere. Sin intervención completa de ambos originales, la aprobación sigue bloqueada.
