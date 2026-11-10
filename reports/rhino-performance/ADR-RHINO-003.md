# ADR-RHINO-003 — correcciones del árbol de accesibilidad

Fecha: 2026-11-10T20:40:02.184102+00:00. Proyecto `rhino-performance`.

**Decisión: approved_with_conditions para conservar el candidato local. Liberación remota: blocked.** Esta autorización no proviene del ADR-002: el propietario autorizó ahora las correcciones locales. No autoriza publicación ni contenido CMS.

## Objetivo y evidencia

Corregir los defectos confirmados de ARIA/nombres/contraste/landmarks y controles de packs reutilizando sus fuentes. Se recuperaron el diagnóstico y los registros anteriores, se leyeron las fuentes actuales y se congelaron hashes antes de editar. [Implementación, archivos y pruebas](accessibility-fixes.md).

## Propuestas, preguntas y respuestas

Claude propuso dos lotes, incluidos contraste y H1. Codex propuso primero semántica/teclado con contraste y H1 separados. Se registraron ocho objeciones en el contraste y seis preguntas; las defensas contienen seis respuestas. Codex adoptó el alcance por lotes. Ambos cuestionaron colores configurados, coexistencia del H1, nombres, consumidores del modal y doble activación/foco del pack.

Resoluciones observables: nombres desde HTML visible; logo con rol de imagen; footer interior div; fuentes de contraste corregidas sin más overrides; checkbox de H1 con contrato editorial explícito; control de teclado delegado al botón/select nativo; foco identificado por producto y control dentro de su catálogo. El rating conserva el label opcional como title, sin nuevos IDs. No se implementó sanitización global de CMS ni un motor alternativo.

## Restricciones y gates

QA estático y de proyecciones aprobado; revisión independiente Claude aprueba el candidato local. El controlador verificó hashes, alcance y ausencia de cambios fuera de los 12 archivos declarados. No hay escrituras comerciales ni operaciones de producción. Los fallos de preparación del helper no se cuentan como participación real.

La coincidencia de los agentes no certifica Tiendanube. La aprobación remota queda bloqueada hasta render real, QA completo de consumidores, visual, teclado y funcionalidad comercial pertinente en un entorno autorizado. La regla de H1 no tiene enforcement automático en el editor. Marca oscura y otros montajes de reseñas exigen revalidación.

## Beneficios, riesgos y reversión

Beneficios demostrados solo en el alcance local: desaparecen las violaciones reproducidas de las reglas seleccionadas, footer con un landmark y controles nativos sin interceptación incorrecta del teclado. No se atribuye mejora de SEO/ventas/velocidad. Los cambios de color requieren aceptación visual; el foco completo del menú y la lista CMS siguen pendientes. Se preservaron motores LS, hooks, destinos, precio, stock y selección.

Dos transacciones con backups/hashes y diff propio permiten reversión sin descartar modificaciones ajenas. No se ejecuta publicación ni la revisión del consejo puede autorizarla.

## Actualización de binding de fuente

Ubicación corregida por el propietario: `~/Escritorio/Cli/Rhino-Ipanema`. Se conservaron sus cambios adicionales y se reaplicó el alcance de accesibilidad sobre su baseline, con QA de componentes, 54 checks estáticos y nueva revisión independiente de Claude. Aprobación limitada al candidato local; publicación sigue bloqueada. Las transacciones propias en la carpeta anterior se revirtieron con hashes, sin tocar cambios ajenos. Ver [registro de traslado](accessibility-fixes.md#corrección-de-ubicación--10-de-noviembre-de-2026).
