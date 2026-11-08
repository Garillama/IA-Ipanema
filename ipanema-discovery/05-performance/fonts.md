# Fuentes y estabilidad tipográfica

Fecha: 2026-11-08. Fuente: style-tokens.tpl y config/settings_data.json. Los valores locales guardados seleccionan Gilda Display y DM Sans; el selector ofrece muchas familias pero eso no significa que todas se descarguen.

El layout declara preconnect a Google Fonts y gstatic y preload de la URL de estilos. style-tokens usa selected_fonts/additional_fonts y pesos por defecto 400,700 con google_fonts_url. Los bloques heading pueden elegir fuente propia. No se encontró un inventario local de WOFF2 del branding: las familias se resuelven externamente. La respuesta de Google Fonts y sus subsets/pesos efectivos deben comprobarse en red.

En la pantalla de acceso observada se cargó Poppins con otros pesos, lo que confirma un contexto visual distinto del setting local. Lighthouse desktop señaló carga de webfonts entre causas de algunos shifts; no demostró que todos los saltos fueran tipográficos. [Informe desktop](../13-evidence/measurements/lighthouse/desktop.json).

Propuesta: limitar familias/pesos realmente usados, comprobar fallback con métricas próximas y reservar geometría de encabezados. `font-display: swap` permite texto inmediato pero puede cambiar métricas; no garantiza CLS cero. Preload de CSS de fuentes no equivale a preload de WOFF2. Precargar solo fuentes imprescindibles y con formato/crossorigin correctos, sin competir innecesariamente con el LCP.

Si se considera alojamiento propio, verificar derechos del archivo de fuente, soporte de assets del tema y mantenimiento de subsets. No descargar ni redistribuir fuentes comerciales basándose en que el editor las muestra. Beneficio y coste deben medirse frente a la entrega actual del CDN.
