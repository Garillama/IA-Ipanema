# ADR-RHINO-009 — rendimiento actual y siguiente intervención

Fecha:2026-11-11T21:09:01.222559+00:00. Proyecto:rhino-performance. Estado:**needs_evidence**. ID nativo del controlador:`ADR-a80ea3cd27c9`. Implementación permitida:**no**. Producción:**no autorizada**.

## Problema y evidencia

Home mediana64 móvil/87 escritorio en5 muestras por dispositivo. TBT móvil alto también en categoría/PDP; colas de CPU atribuibles principalmente a integraciones de medición. Header pasa de flujo normal a absoluto y mueve MAIN74px en escritorio. [Mediciones y condiciones](performance-renewal-20261111.md); [baseline](performance-baseline-20261111.json).

## Alternativas y contraste

Claude propone atribuir TBT primero; header inicial y reserva de controles son candidatos distintos. Codex inicialmente prioriza header inicial y después cambia a atribución de TBT por la prioridad móvil. Ambos conservan Sectionfy, Swiper, SEO y contratos comerciales. Hubo6 preguntas/6 respuestas/14 objeciones; [registro completo](performance-renewal-council.json), con propuestas independientes, defensa, modelos y costes observados.

La traza nueva respalda investigar Google Tag/Analytics, Meta y TikTok; no justifica retirar tracking ni reescribir componentes del tema. El A/B del header elimina el salto geométrico observado en escritorio y conserva geometría/fuentes finales, sin demostrar mejora global de score. El candidato sigue separado de la solución verificada.

## Decisión

1. Conservar las optimizaciones actuales y todos los cambios locales ajenos.
2. No aplicar todavía el [candidato CSS](header-initial-flow-candidate.patch). La autorización local existe, pero falta cerrar la aceptación exigida por las objeciones. El acuerdo no sustituye los recibos.
3. El contrafactual de Google ya se ejecutó: tres controles y tres bloqueos locales, exceso de tareas en ventana20s con mediana2022→1356ms. No es TBT oficial ni una solución con tracking preservado. Continuar la evaluación acotada de cada tag; cualquier ajuste remoto de GTM/apps requiere autorización específica y validación de eventos comerciales/consentimiento. No eliminar funcionalidades para lograr90.
4. Para el header: demostrar procedencia/compatibilidad del template y CSS compilado, comparar Lighthouse antes/después con5 muestras/dispositivo y perfil idéntico, cerrar foco/sin JS/variantes y revisión independiente del diff exacto. La prueba temporal no autoriza publicar.
5. Preservar el baseline nuevo para activar gates solo después de probar una comparación compatible y sus tolerancias. PSI/CrUX actuales quedan bloqueados por claves no heredadas, no por supuesto fallo de la tienda.

## Riesgos y límites

Cambiar tags puede perder atribución, eventos o consentimiento; modificar header puede afectar menús, scroll o elegibilidad de páginas futuras. El pico CLS1.0045 aún no tiene causa raíz demostrada. No hay mejora móvil atribuible al CSS. No hay INP nuevo ni certificación WCAG/indexación/carrito. No se alteró el tema ni se ejecutaron operaciones remotas de escritura.

Se conserva evidencia de todos los proveedores originales; el controlador devolvió `implementation_allowed=false`, deliberación completa y aprobación incompleta. Reversión actual:no necesaria, no hubo aplicación; una futura aplicación debe usar transacción/backups y hashes propios.


## Actualización — cierre local del header, 11 de noviembre de 2026

El estado inicial anterior se conserva como historial. La subdecisión del header v2 pasa a **approved_with_conditions**, con implementación local aceptada en la transacción `81a54d213d92470783a55a5eb2f55689`, revisión independiente real y hash verificado. [Informe, pruebas y limitaciones](adr009-followup.md) · [diff exacto](header-initial-flow-v2.patch). El candidato v1 queda supersedido. No autoriza producción. Las decisiones sobre marketing y el objetivo 90+ siguen **needs_evidence**; no se retiró ninguna integración.
