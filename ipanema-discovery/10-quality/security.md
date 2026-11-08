# Seguridad, permisos y mantenibilidad

Fecha: 2026-11-08. Revisión estática y de superficies autorizadas; no se realizó pentest, explotación ni auditoría de dependencias contra una base de vulnerabilidades.

Se mantuvo el origen en lectura. La contraseña de storefront se utilizó tras autorización del propietario en un navegador aislado; no se guardaron cookies, contraseña ni tokens en evidencias. Las credenciales del CLI se consumieron por el ejecutable ya configurado, sin copiarlas al repositorio. El listado de temas se redujo a los registros necesarios, sin revision_token.

`blocks/code.tpl` y `settings.css_code` imprimen contenido raw. La facultad de insertar código es real y debe reservarse a contenido confiable; no se interpreta como vulnerabilidad demostrada por sí sola. Richtext, descripciones de producto, URLs y JSON-LD requieren considerar el escape del contexto. Un escape válido para HTML no es necesariamente válido para JSON dentro de script.

El macro json_string utiliza json_encode con flags; Organization tiene escape manual. Los mensajes de preview validan la fuente parent y un tipo permitido. Los mensajes de vídeo comparan contentWindow y algunas rutas parsean JSON. Antes de cambiar esas ramas, mantener validación del emisor y manejar payload inesperado; no eliminar controles por simplificar una animación.

El JS descargado de plataforma o de apps tiene autoridad en la página. Revisar proveedor, necesidad, duplicación, consentimiento y mantenimiento. No insertar tokens Admin/API dentro del tema, settings de código o URL pública. LS y rutas internas observadas no sustituyen una API pública con permisos y estabilidad.

No se encontró una licencia de redistribución del tema en el origen. Reutilizar conocimiento e interfaces no concede permiso para copiar código entre comerciantes. Para módulos propios, registrar autoría/licencia y separar dependencias de Tiendanube. Para imágenes/fuentes/marcas, comprobar derechos de esos assets por separado.

No se instalaron dependencias nuevas ni se alteraron roles/permisos/apps. La antigüedad de un banner de librería no prueba una vulnerabilidad concreta; hace falta una versión/artefacto identificado y una fuente de vulnerabilidad pertinente. Los riesgos de fork/actualización están en [regresiones](regression-risks.md).
