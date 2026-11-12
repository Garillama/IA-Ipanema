# Conciliación administrativa y cobertura Google — solo lectura

## Categorías y subcategorías

No se identificó una integración administrativa autorizada en el proyecto ni un conector Tiendanube disponible en este runtime. La CLI de temas no acredita acceso al catálogo administrativo. No se reutilizan sus credenciales para inventar otra integración.

El propietario puede abrir **Productos > Categorías**, ruta documentada por [Tiendanube](https://ayuda.tiendanube.com/es_MX/122709-categorias/como-ocultar-una-categoria-de-productos-de-mi-tiendanube), y expandir el árbol completo sin arrastrar, ocultar, mostrar ni guardar elementos.

Completar [la plantilla](admin-category-reconciliation.csv) para cada categoría y nivel real, incluidas las que no estén entre las cinco conocidas. Registrar nombre, padre, nivel, URL exacta y los valores de visibilidad/publicación que el panel muestre. Anotar ID únicamente si aparece. Si el panel no expone un estado o identificador, registrar «no expuesto», sin deducirlo de la presencia en el sitemap. Guardar fecha y evidencia local sin cookies, cabeceras o datos de clientes.

Separar visibilidad en navegación de respuesta pública/indexabilidad: ocultar una categoría no equivale a ocultar sus productos y puede afectar a sus subcategorías, según la documentación citada. Una categoría oculta no debe promoverse automáticamente. «No publicada» se utiliza solo si existe evidencia administrativa de ese estado; no se inventa como sinónimo de ausencia del sitemap.

Cruzar cada URL contra la matriz: conocida y coincidente; pública adicional por verificar; oculta/no publicada según panel; URL ausente o ambigua. No recorrer automáticamente las nuevas rutas ni alterar menús. La plantilla está basada en nombres/rutas públicas, **no es una exportación ni un inventario administrativo completado**.

## Search Console: exportación oficial

Seleccionar la propiedad **sc-domain:rhino-performance.com**, abrir **Indexación > Páginas**, registrar fecha y filtros y exportar el resumen. Abrir también cada motivo relevante para exportar sus ejemplos de URLs: descubiertas/rastreadas sin indexar, redirecciones, duplicadas/canonical alternativo, noindex, bloqueadas, 404 y errores de servidor. Conservar los archivos originales y los totales visibles, no solo capturas parciales.

Google ofrece CSV, Excel y Hojas de cálculo mediante el botón de exportación. La descarga está limitada a ejemplos —hasta 1000 filas— y los totales pueden incluir URLs no exportadas. El informe de Páginas tampoco garantiza que se muestren todos los ejemplos incluso por debajo de ese límite. No tratar un archivo como censo completo. Fuentes oficiales: [exportar informes](https://support.google.com/webmasters/answer/12919797?hl=es) e [Indexación de páginas](https://support.google.com/webmasters/answer/7440203?hl=es).

No pulsar «Validar corrección», solicitar indexación ni enviar sitemaps como parte de esta preparación. No compartir enlaces de sesión, cookies o tokens. Los cuatro próximos casos de URL Inspection ya están definidos en [el plan existente](../google-coverage-plan.json); solo se ejecutarán con acceso disponible y autorizado, sin repetir las quince inspecciones conservadas.
