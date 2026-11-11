# ADR-RHINO-007 — batching de medición de reseñas de Home

Estado: **blocked para aplicación; candidato probado en sandbox**. Fecha:2026-11-11T00:34:12.858365+00:00. Seguimiento acotado de [ADR-RHINO-006](ADR-RHINO-006.md). Proyecto:rhino-performance.

## Objetivo y alcance

Reducir lecturas/escrituras intercaladas en `setupMore`, sin cambios de apariencia, contenido, API, eventos, ARIA o comercio. Único archivo candidato del tema: `sections/google-reviews.tpl`. El padre es una tarea L3; este lote localizado esL2 con contraste solicitado de los dos proveedores.

El usuario autorizó iniciar el lote local y, tras el fallo de Claude, eligió continuar **solo pruebas y dejar la aplicación pendiente**. Esa es la autorización vigente. No producción ni edición del tema en este cierre.

## Evidencia y propuestas

Dos perfiles CPU×4 observaron setupMore~156/45ms. La fuente contiene lecturas geométricas seguidas de cambio de clase para cada tarjeta. Codex propone separar lecturas/escrituras y evitar cambios de clase redundantes; también reconoce que mostrar botones puede afectar geometría compartida, por lo que exige pruebas.

Claude no produjo propuesta:2intentos reales con error de autenticación, procesos finalizados, sin timeout ni análisis generado. No hay opinión, voto, contraste o revisión de Claude en este lote. No se heredan aprobaciones anteriores ni se activa CommandCode.

## Candidato, alternativas y pruebas

Candidato: array de estados en primera pasada y aplicación condicional de `has-more` en segunda. Alternativa segura: conservar lo actual. Aplazar fetch de reseñas/introducir observers cambiaría más contratos y no forma parte del lote.

13checks fuente-componente pasan en6anchos; estados y capturas equivalentes con máscaras explícitas de avatares incompletos.5mediciones por variante/ancho reducen3–4layouts a1. Los12ensayos de página completa usan un perfil intervenido que altera transferenciaHTML; no pueden demostrar el score de producción ni una mejora global. Los prototipos sin DOMfiel se descartaron.

## Decisión y condiciones pendientes

Conservar el candidato y evidencia, **sin aplicar al tema**. Hay mejora localizada, pero no evidencia de90+ o beneficio global suficiente para afirmarlo. Continúan desconocidas la aprobación de Claude, compatibilidad completaTwig/plataforma y mejora global bajo condiciones reales de publicación.

Para reabrir: usuario habilita la siguiente fase; validar fuente/hashes; recuperar Claude; completar deliberación acotada y revisión independiente del diff; resolver cualquier objeción con pruebas del controlador. Si se acepta localmente, usar transacción sobre ese archivo y verificar hashes, diff y QA. Medir entorno de prueba compatible y validación publicada únicamente tras push del propietario/autorización específica. No repetir discovery ni reconstruir el orquestador.

Reversión actual: no necesaria porque el tema no fue modificado. El borrador está aislado. No se garantizan puntos, CWV o indexación. [Informe y evidencia](home-js-first-batch.md).
