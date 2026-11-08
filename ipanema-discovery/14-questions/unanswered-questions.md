# Preguntas técnicas abiertas

Fecha: 2026-11-08.

- ¿Por qué la plataforma selecciona assets de 1.2.1 para password y 1.8.0 tras desbloquear? La observación está probada, la causa interna no.
- ¿Qué restricciones adicionales aplica el editor a code/custom y bloques privados? La ayuda y el schema local no describen exactamente el mismo límite; falta Admin en lectura.
- ¿Cómo se resuelve la carga posterior de categoría en el escenario registrado? La prueba no aumentó tarjetas; no se atribuye causa sin traza/reproducción adicional.
- ¿Qué IDs generados por block_attributes deben ser únicos globalmente y qué corrección soporta plataforma? Hay duplicados medidos; no se cambió el contrato del editor.
- ¿Qué aplicaciones están instaladas y cuáles tienen acceso a slots, tracking o datos privados? Network solo muestra lo cargado en el recorrido.
- ¿Cuál es el INP y LCP p75 de usuarios reales y su distribución por dispositivo? No hay datos de campo consultados.
- ¿Qué pasa con estados de stock agotado, variantes inválidas, kits/suscripciones y error de envío en datos controlados? Source revisado, no simulación transaccional.
- ¿Cuál es la compatibilidad completa de la implementación con otros navegadores y lectores de pantalla? Chrome/emulación no lo demuestra.
- ¿Qué diferencias exactas hay entre este código y el release oficial intacto de Ipanema 1.8.0? La sincronización con la tienda no responde esa pregunta.

Cada pregunta conserva el impedimento y la prueba que la resolvería en la [matriz QA](../10-quality/testing-matrix.md); no se reemplaza con una suposición.
