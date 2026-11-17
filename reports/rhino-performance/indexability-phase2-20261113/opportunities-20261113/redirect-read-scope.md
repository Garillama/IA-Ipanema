# Redirecciones: alcance mínimo pendiente, sin autorización de ejecución

Prioridad documental: las cinco URLs exactas de [legacy-top-five.json](legacy-top-five.json), ordenadas por clics históricos. No son rutas privadas. Los destinos no se deducen ni se precargan.

Objetivo de una comprobación futura: obtener HTTP y Location de cada origen, cada salto seguro permitido, HTTP final, canonical y contenido final para verificar correspondencia. Una respuesta 3xx correcta no es un defecto. No visitar enlaces de navegación ni recursos de página.

Reutilizar exclusivamente el transporte y supervisor integrado. Antes de cualquier ejecución: revisar hashes vigentes, selección cerrada, robots.txt, origen y marcador de ejecución única; preparar el manifiesto y comando reales mediante el mecanismo existente, y obtener autorización específica. Este documento NO es una invocación ni autorización.

Límites conservadores de referencia: 12 GET totales incluyendo robots y saltos; concurrencia 1, máximo 0,5/s o menor según robots; 120 s supervisados; timeout20 s; cuerpo codificado/descomprimido máximo2.000.000 bytes; tres saltos globales; parada ante403/429, robots desconocido/denegado, TLS/IP/origen/redirección inseguros, timeout o presupuesto agotado. Sin reintentos, Google, home adicional, sitemap ni recursos. `/home/` figura como destino histórico específico; no equivale a permiso para añadir `/` fuera de un salto permitido.

Condición pendiente: el selector actual requiere cinco URLs. Con tres saltos globales no se puede prometer completar cinco cadenas de redirección. No ejecutar hasta definir si se autorizará un resultado parcial acotado o un presupuesto revisado explícitamente. No modificar el motor para resolver esta planificación. Hasta entonces: `needs_evidence`, sin comando ni permiso de red nuevos.

Una conclusión válida puede ser «redirección conservada y temática», «defecto reproducido» o «cadena incompleta por presupuesto». La última jamás se convierte en aprobación o fallo comercial demostrado.
