# ADR-RHINO-008 — medios Sectionfy en carrusel y banner

Fecha: 2026-11-11T19:31:01.071998+00:00. Estado **approved_with_conditions para código local opt-in**, aplicado y aceptado. La conexión/activación real y producción quedan fuera de esa aprobación. No autoriza producción.

## Objetivo y decisión propuesta

Fotos en Tiendanube y videos desde Sectionfy. Se conserva el carrusel Swiper y el helper de imagen. Un único consumidor de archivo HTML5 sirve al slide y, mediante una adición acotada, al banner actual. Se mantienen las fuentes anteriores como predeterminadas; no se migra ni configura Home automáticamente.

## Investigación y contraste

La PDP utiliza product.video_url/fallback YouTube/Vimeo; su conexión Sectionfy se usaba para FAQ, specs y rich_description, sin VIDEO_BANNER. El carrusel admitía fotos y no archivos de video. Ambos participantes propusieron soporte opt-in sobre Swiper y señalaron acoplamiento de loop/autoplay, pérdida de claves en pick, redirecciones y capas/foco. Hubo cinco preguntas y sus respuestas. La fase de fuente no acreditó funcionamiento ni dio autorización de publicación.

Se seleccionó como dirección técnica la alternativa nativa `codex-native-mixed-optin`; la identidad del proveedor no justificó la elección. El candidato reutiliza un loader compartido con selección exacta y un solo consumidor. La adición al banner permite conservar la sección actual sin migrar la configuración protegida. La revisión posterior de ambos participantes aprobó el diff completo corregido, incluido el host del banner.

## Evidencia y defectos

222 comprobaciones finales pasaron:153 de componente,37 del cliente,8 de decodificación real local y24 de fuente. API simulada en las pruebas; una consulta externa real devolvió403. El defecto de sincronización del temporizador se reprodujo y corrigió. Codex objetó el overlay; está corregido y probado, y posteriormente recibió aprobación explícita de ambos participantes. No se certifican Twig, marca visual publicada, archivo del cliente, cuotas Google ni velocidad90+.

## Gate actual

El rechazo previo de cuota de Claude y la objeción de overlay se conservaron como historial. En la reanudación solicitada, Claude y Codex aprobaron de forma real el diff corregido, solo para fuente local opt-in. No se sustituyó al revisor independiente. Las pruebas posteriores sobre el tema real pasaron:153 de navegador,37 del cliente,8 de decodificación local y11 controles de hashes/archivos protegidos en el recibo.

La transacción `74287aba4f02488d9878fbcc74cbd18b` se aceptó tras verificar backups, hashes y baseline real de capacidad ausente. No autoriza publicación ni afirma funcionamiento del endpoint/archivo comercial. Los campos nuevos quedan con defaults anteriores y URL vacía; la instancia de Home y los cambios previos del propietario siguen intactos.

## Reanudación y reversión

Mantener hashes y copias originales. La revisión y transacción local ya se completaron. Retomar desde la aceptación: configurar la consulta pública real y validar el render/archivo antes de activar en vivo; no reiniciar el discovery. La reversión debe usar solo los archivos de esta transacción si sus hashes siguen coincidiendo. Si el original cambió, resolver el conflicto sin sobrescribirlo. La configuración y validación real de Sectionfy permanecen separadas de cualquier autorización de publicar.

[Informe principal](sectionfy-hero-media.md) · [Revisiones](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/source-review.json) · [Patch](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/ready-local.patch) · [Checkpoint](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/checkpoint.json).

## Adenda: fuente Home automática verificada

El propietario proporcionó la ruta pública correcta de Home en sectionfy.codefy-apps.com. Se verificaron HTTP200, CORS y reproducción del MP4 real desde un frame temporal del origen Home. El delta L2 recibió revisión independiente de Claude y se aplicó localmente con la transacción `827e410704fc48b8be9c7753e17c294b`, aceptada tras199pruebas funcionales posteriores y10controles de archivos/hashes. Home ya no necesita URL manual: reutiliza el token público existente y selecciona el modo Sectionfy en el banner principal. Sin publicación ni cambios de la app. La revisión completa de velocidad/diseño desplegados permanece posterior a la actualización del propietario. [Estado actual](sectionfy-automatic-home.md).
