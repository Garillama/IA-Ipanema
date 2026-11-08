# Presupuestos propuestos

Fecha: 2026-11-08. **Son objetivos iniciales de ingeniería, no mediciones ni límites nativos de Tiendanube.** Se ajustarán con una línea base del storefront y requisitos comerciales. Se contabiliza transferencia comprimida con caché fría, separando tema, plataforma y terceros.

| Recurso / resultado | Objetivo inicial | Verificación / límite |
|---|---|---|
| JS del tema inicial | ≤150 KiB transferidos | Excluir y reportar aparte JS de plataforma; medir por ruta, no sumar source Twig |
| Delta de una sección nueva | ≤5 KiB JS gzip; preferir 0 si es presentación | No cargar biblioteca completa para un cambio de layout |
| CSS del tema transferido | ≤60 KiB; delta por sección ≤2 KiB gzip | CSS inline cuenta dentro del documento y no se ignora |
| Imagen visual principal | ≤200 KiB mobile, ≤350 KiB desktop | DPR/calidad visual y formato negociado; no degradar producto a ciegas |
| Imágenes antes del primer scroll | ≤400 KiB mobile, ≤700 KiB desktop | Distinguir solicitadas y completadas; registrar ocultas |
| Fuentes | ≤2 familias, ≤3 archivos críticos, ≤120 KiB | Subsets pueden generar más archivos: medir lo realmente requerido por texto |
| Solicitudes iniciales | Objetivo ≤50 | Plataforma y apps se muestran por separado; el número solo no define rapidez |
| Terceros | 0 scripts duplicados; cada proveedor con función/consentimiento y coste registrado | No fijar reducción por eliminar medición necesaria sin decisión del negocio |
| Tareas nuevas del tema | Evitar tareas ≥50 ms; handlers de interacción con trabajo acotado | CPU móvil real/simulada, no solo desktop potente |
| LCP/INP/CLS de campo p75 | ≤2.5 s / ≤200 ms / ≤0.1 | Móviles y desktop separados; requiere datos de campo |
| FCP / respuesta servidor de laboratorio | Objetivo ≤1.8 s / ≤0.8 s en perfil acordado | Dependen del hosting/plataforma; no prometer control desde CSS |
| Regresión tras cambio | Sin aumento material injustificado de bytes, solicitudes, shifts o trabajo de interacción | Comparar mismo estado, perfil, datos y varias muestras cuando haya variación |

Una superación justificada se documenta con beneficio UX/comercial, coste, alternativas y responsable de mantenimiento. No bloquear una función nativa por un presupuesto inventado sin línea base. La prioridad inmediata es evitar duplicaciones nuevas y medir recursos ocultos, mientras se establecen números reales de las páginas desbloqueadas.
