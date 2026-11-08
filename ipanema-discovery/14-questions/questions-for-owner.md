# Decisiones del propietario basadas en evidencia

Fecha: 2026-11-08. Son decisiones para una fase posterior; no bloquean la documentación realizada. Ya se recibió autorización de acceso al storefront y no se vuelve a pedir esa contraseña.

| Decisión concreta | Hallazgo que la motiva | Por qué importa |
|---|---|---|
| ¿Qué imagen, título y destino sustituirán el contenido de ejemplo del hero? | IPN-011: el placeholder actual es LCP | La optimización debe medirse con el medio final y no solo el ejemplo |
| ¿La carga incremental del catálogo es un requisito comercial o se acepta paginación nativa clásica? | IPN-009: infinite activo sin href siguiente | Ambas necesitan descubrimiento real; cambia el trabajo necesario para conservar la UX |
| ¿Qué persona/proceso mantiene actualizaciones del fork 1.8.0? | IPN-001 y estado remoto: ya existe fork | La decisión pendiente es mantenimiento de ese fork, no si hacer el primer fork |
| ¿Las descripciones importadas pueden normalizarse editorialmente conservando su contenido? | IPN-007: nueve PDP con H1 de descripción y estilos de otro constructor | Permite resolver el origen semántico sin parches CSS |
| ¿Qué variantes de layout deben poder editarse desde Admin y cuáles deben quedar como reglas de marca? | IPN-023 y matriz de 708 controles | Evita agregar campos arbitrarios o duplicar configuraciones por tienda |
| ¿Hay permisos para distribuir código del tema entre otras tiendas o solo patrones/código propio? | IPN-022 | Define qué puede formar parte de una biblioteca compartida |
| ¿Qué contenidos del blog de prueba deben conservarse antes del lanzamiento? | Crawl de siete posts, algunos títulos repetidos/de prueba | Requiere decisión editorial; no corresponde eliminarlos por una auditoría técnica |
| ¿Qué catálogo/cliente/escenario de prueba se usará para stock, cupones, compra y checkout? | Matriz QA: esos estados no se modificaron | Hace posible validar sin confundir pruebas con operación comercial |

Los principios de reutilizar componentes, evitar JS innecesario, mantener rapidez y no acumular !important ya son requisitos del propietario; no se vuelven a presentar como decisiones opcionales.
