---
name: ipanema-storefront
description: Coordinar discovery y cambios de temas seccionables Ipanema de Tiendanube, seleccionando capacidades, conocimientos y QA según la petición. No usar reglas de este modelo para temas clásicos o Shopify.
---

# Coordinadora Ipanema

La raíz es `../../..` desde esta skill. Sigue [AGENTS.md](../../../AGENTS.md), selecciona el proyecto con `python3 tools/ia.py projects list` y comprueba `doctor` cuando necesites archivos o navegador. No cargues todo el discovery.

Usa `route "petición"` para orientación y `search "componente o problema" --limit 3` para recuperar fuentes, consumidores, settings, fecha y soluciones. Contrasta candidatos con el código real. El router no sustituye tu juicio ni invoca agentes. Una configuración ausente exige investigación, nunca afirmación de soporte.

Selecciona solo las especialidades pertinentes: architect para dependencias/alcance; component-builder para composición/schema; seo-expert para HTML/rastreo; performance para red/ejecución; responsive para cascada/dispositivos; motion para efectos; visual-qa para pruebas/comparaciones; commerce para contratos de compra. Cada una vive en su directorio hermano. Por ejemplo una card suele involucrar architect, component-builder, responsive y commerce; SEO de un carrusel requiere seo-expert y la fuente del componente, no todas las skills.

Para cambios no triviales usa `plan "petición" --action local-change --authorize-local --save` dentro del alcance autorizado y completa evidencia, consumidores y pruebas antes de editar. Sigue la mínima intervención de AGENTS. Los niveles de permiso y autocorrección están centralizados allí; no hay publicación automática.

Comprueba QA proporcional. `qa --suite quick` valida el agente; `qa --suite page --page home` o `component --component "selector"` valida un entorno preparado. Añade `--allow-network` únicamente si está autorizado el acceso remoto de lectura. `compare` contrasta PNG o métricas; `attempt` controla correcciones locales. No apruebes pruebas no ejecutadas.

Entrega objetivo/decisión, fuente nativa, diff, pruebas, comparación y pendientes. Finaliza cuando el alcance esté verificado o documenta qué impidió comprobarlo. [Manual](../../../README.md), [arquitectura](../../../reports/v2/architecture.md).

Cuando se solicite coordinación de Claude Code y Codex aplica el [orquestador](../../../reports/orchestration/README.md). `orchestrate task "petición"` recupera contexto y propone DAG/riesgo/archivos; `--execute` inicia inferencia real dentro de autorización aplicable. Consulta la participación vigente en `tools/ipanema/orchestration/models.json:council`; la skill no puede habilitar proveedores desactivados. No activar el consejo para L1 sin necesidad ni repetir investigaciones. Verifica candidatos, independencia de revisiones, SHA256 y pruebas; no confundir un diff aislado con una modificación publicada o una aprobación completa de storefront. Ante fallos no eleves permisos ni asumas pruebas ejecutadas. Los detalles de CLI/modelos viven en el registro fechado del módulo, no se duplican en la skill.
