# Comprobación limitada propuesta de los 20 artículos

No ejecutada ni autorizada. No reabre la cobertura HTTP (124/124). La búsqueda acotada de 203 archivos de familias de captura originales conserva HTTP/canonical/breadcrumbs, pero no recuperó meta robots, X-Robots-Tag ni main. Un hash del HTML no reconstruye su cuerpo; tampoco prueba ausencia de noindex. [Recuperación y procedencia](twenty-original-recovery.json).

Se prepararon cuatro manifiestos de cinco URLs mediante el selector nativo existente, sin modificar el motor. Cada ejecución requiere autorización propia. La necesidad de un GET nuevo es obtener los campos no retenidos; no volver a demostrar simplemente HTTP 200 ni repetir las 124 páginas.

| Operación | URLs | SHA256 | Comando |
|---|---:|---|---|
| 01 | 5 | `77115227846b88a06aa97f62d73ead43ee007ab8c0db7b9f72cdb4958f865232` | [Comando exacto](technical-completion-01/command-NOT-AUTHORIZED.txt) |
| 02 | 5 | `bb15cf37dce574107be9dd767768827c351775dec651eb6e1ea62c3708d0f46c` | [Comando exacto](technical-completion-02/command-NOT-AUTHORIZED.txt) |
| 03 | 5 | `922631b61146275e73f8b1c4d221f2e265aead78f2d9ca578bf4864564305193` | [Comando exacto](technical-completion-03/command-NOT-AUTHORIZED.txt) |
| 04 | 5 | `3f9bd756c98c6121496323abace180b2eac19aef654f868469068fe2781fd56d` | [Comando exacto](technical-completion-04/command-NOT-AUTHORIZED.txt) |

Por operación: 12 GET máximos incluidos robots y redirecciones; concurrencia 1; máximo 0,5/s o menor según robots; supervisor absoluto 120s; timeout 20s; 2.000.000 bytes codificados y descomprimidos; tres redirecciones globales. Solo cinco destinos y robots, sin home/sitemap/assets/GSC. Parada global ante403/429, robots desconocido/denegado, TLS/IP/origen/redirecciones inseguros, timeout, error crítico o presupuesto agotado; cero reintentos automáticos.

**Preflight distinto de los lotes anteriores:** estos destinos ya tienen HTTP 200. Debe comprobar campos faltantes y procedencia, no exigir `http=not_observed`. Los drivers locales de lotes01–15 no se deben reutilizar sin ajustar ese control de propósito. El CLI, transporte y presupuestos permanecen iguales. Usar marcador propio de un solo uso y checkpoint nativo independiente; no modificar los marcadores consumidos.

Después se conservarán las observaciones nuevas con su fecha sin sobrescribir las antiguas ni cambiar el historial GSC. Si alguna señal se recupera antes desde archivos guardados, detener y conciliar el manifiesto antes de pedir su autorización. No aprovechar presupuesto sobrante para otras URLs.

No se solicita autorización conjunta para las20. La primera operación pendiente figura con sus cinco URLs exactas en [targets.json](technical-completion-01/targets.json); autorizarla no habilita las otras tres ni modifica la tienda.
