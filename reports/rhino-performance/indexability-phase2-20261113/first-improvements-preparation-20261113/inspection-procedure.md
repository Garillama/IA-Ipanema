# Dos inspecciones oficiales — procedimiento preparado, sin ejecutar

## Acceso y alcance

El controlador ejecutó únicamente `python3 tools/ia.py --project rhino-performance access doctor`, sin probe. Resultado local: GSC configurado, `credential_available=false`, cuenta/API no comprobadas. No se intentó la API, no se abrió OAuth y no se recuperaron credenciales. No se afirma que el propietario carezca de acceso en su navegador.

Se utilizarán resultados oficiales que proporcione el propietario. Si luego se habilita la integración autorizada, dos lecturas API requerirán su alcance específico y credencial válida, sin nuevas autenticaciones implícitas. No se inventa una invocación para una credencial que no está disponible.

## Operación manual exacta

1. En la sesión propia de Search Console, seleccionar la propiedad de dominio **rhino-performance.com**.
2. Introducir en la barra de Inspección de URLs, sin modificar la ruta:
   - `https://rhino-performance.com/terapia-fria/`
   - `https://rhino-performance.com/productos/brazo-presoterapia-pro-3-individual/`
3. Abrir por separado el resultado almacenado/indexado de cada URL. No pulsar «Probar URL publicada», «Solicitar indexación» ni «Validar corrección» como parte de este alcance. Una prueba en vivo sería una comprobación diferente y no demostraría indexación.
4. Conservar fecha y hora de consulta con zona horaria y la URL exacta. Copiar el estado y motivo literal y desplegar los detalles de indexación que estén disponibles:
   - permiso de rastreo/robots;
   - obtención de página y su estado;
   - indexación permitida;
   - último rastreo y agente, si constan;
   - canonical declarado por el usuario;
   - canonical elegido por Google;
   - sitemap o página de referencia, si aparecen.
5. Si una URL no tiene información suficiente, conservar «N/D» o el mensaje literal. No sustituirlo por una conclusión de bloqueo o por la fecha del archivo. El valor antiguo25568 de las exportaciones sigue siendo una fecha no utilizable de rastreo.
6. Entregar capturas de los resultados y detalles, o copiar los campos en un archivo local. No hace falta una exportación XLSX que la interfaz no ofrezca. No proporcionar cookies, tokens, claves o enlaces privados de sesión. Los dos resultados pueden guardarse en un PDF desde el navegador con la URL y la fecha anotadas.

## Interpretación posterior

Guardar cada observación con su fuente, SHA256, fecha y versión de la prueba. Contrastar con las respuestas técnicas conservadas sin reemplazar sus fechas. Un canonical elegido distinto requiere analizar la identidad de ambas páginas; un fallo de obtención requiere evidencia de su naturaleza; «Descubierta sin indexar» no demuestra por sí sola una carencia editorial o fallo del tema. Si canonical o último rastreo no están disponibles, quedan desconocidos.

El informe oficial almacenado ayuda a entender el estado conocido por Google; no verifica la obtención actual del storefront. Las observaciones HTTP200 previas tampoco prueban que Google haya rastreado o indexado las URLs después.

## Qué requiere autorización

Recibir y leer archivos locales de esos resultados ya está dentro del encargo. Nuevas lecturas por API, pruebas en vivo, llamadas al storefront o recuperación de autenticación necesitan autorización aplicable separada. Ninguna de estas acciones solicita indexación o cambia la tienda automáticamente.
