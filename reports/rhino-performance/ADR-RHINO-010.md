# ADR-RHINO-010 — peso publicado y rendimiento habitual

Estado: **needs_evidence para intervención remota**. Participante: Codex únicamente, por instrucción del propietario. No hubo consejo, revisión independiente simulada ni aprobación de producción.

## Evidencia

[Informe y fuentes](production-weight-20261112/README.md) · [PDF](production-weight-20261112/informe.pdf) · [Verificación](production-weight-20261112/verification.json).

Se conservaron 130 respuestas PSI (129 mediciones únicas): seis páginas con diez consultas por dispositivo; Home con cinco por dispositivo y una repetida de escritorio. Home móvil: peor49, media69, mediana71, mejor86. El total reportado permanece próximo a2,803MB. Desktop: media79, mediana77, mejor96; peso mediano10,716MB, del cual7,689MB corresponde al MP4.

La diferencia frente al PDF histórico no demuestra un aumento real de descarga: faltan inventario/perfil históricos, y las respuestas PSI actuales contabilizan tamaños no nulos en filas cacheadas. El navegador publicado confirmó una segunda respuesta del SDK de reseñas desde caché. No se asume una segunda descarga física ni dos widgets simultáneos.

## Decisión técnica

1. Priorizar JS/apps y coste inicial móvil, preservando tracking, consentimiento y comercio. No retirar SDK ni deduplicar inicializaciones sin identificar lifecycle y contratos reales.
2. Conservar el helper de imágenes nativo. Usar los mecanismos documentados para imágenes soportadas; no aplicar endpoints inventados a R2 ni al CDN del blog.
3. Conservar el guard de header y la reproducción/pausa condicional, observados publicados. Los dos JS Sectionfy inspeccionados coinciden por hash con los locales.
4. Se prepararon candidatos del mismo MP4:5,869MB y3,866MB, con1920×1080/24fps/20,416667s. Sus ahorros de archivo son23,67% y49,72%; no son mejoras PageSpeed publicadas. El candidato de mayor compresión requiere aprobación visual en movimiento.
5. No hay cambio remoto autorizado ni parche aplicado en esta fase. Revisar la calidad, consumidores, backup y diff/manifest exacto antes de solicitar autorización específica. El archivo original está preservado.

## Condiciones pendientes

- Causa y comportamiento de la segunda carga de recursos de reseñas; acceso/configuración soportada de la aplicación cuando corresponda.
- QA de eventos comerciales y consentimiento antes de cualquier ajuste de medición.
- Revisión humana de los candidatos y de cualquier cambio de alto riesgo mientras Claude no participa. No se desactivan gates.
- Validación posterior únicamente sobre producción tras autorización y despliegue exactos; varias muestras compatibles, incluyendo peores resultados y medias.
- No se demuestra 90+ habitual ni se atribuyen diferencias históricas a parches sin evidencia comparable.

No se crearon clones ni staging, no se modificaron configuraciones remotas ni se ejecutaron push/watch/publish.
