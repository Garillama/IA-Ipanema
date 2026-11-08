# Auditoría inicial y plan SEO

Fecha: 2026-11-08. HEAD `4137374`; archivos versionados limpios y siete archivos SEO previos sin seguimiento. Se conservaron sus hashes antes de evolucionarlos. [Baseline](evidence/initial-baseline.json).

La V2 dispone de configuración multitienda, skills, inventario/grafo, QA Chrome/axe/Lighthouse y reglas de autorización. Su QA inspecciona H1, canonical, enlaces y parseo JSON, pero no valida grafo, elegibilidad por experiencia ni consistencia comercial completa. No hay herramientas conectadas GSC, GA4, Merchant o Chrome DevTools MCP disponibles en esta sesión.

El inicio de tools/ipanema/seo contiene extractor, grafo, consistencia, reglas Google, validador y analizador de ramas Twig. No está conectado a CLI, QA o pruebas. Se reutilizará, corrigiendo límites: anchor sin href omitido, microdata/RDFa incompletos, referencias @id externas tratadas como errores, reglas de carruseles incompletas y estados aprobados sin entidades presentes. Una simulación de Twig no se presentará como ejecución de la plataforma.

En el tema real disponible se encontraron dos snippets JSON-LD y cuatro consumidores literales: layout (dos includes), card y blog-post-item. Los metadatos del head proceden de component('head-tags'). El snippet mantiene la coma condicionada a template != home antes de un bucle potencialmente vacío. Se verificará con código actual, simulación acotada y evidencia capturada; el diagnóstico histórico solo es referencia.

## Plan y aceptación

1. Inspeccionar snippets/consumidores y documentación primaria actual. Registrar reglas fechadas y distinguir carrusel tradicional/beta, datos válidos y presentación en Google.
2. Integrar extractor y grafo; cuatro niveles con estados no comprobados y fuentes. Incorporar metadatos, rastreo, categorías, PDP/variantes, home/blog y comparación HTML/DOM.
3. Generación desde contrato de datos con procedencia y pertenencia a proyecto. Reusar entidades existentes, serializar de forma segura y rechazar campos comerciales ausentes o de otra tienda. Preparar corrección mínima del bug confirmado como artefacto revisable, sin editar el tema real.
4. Reusar el navegador V2 para capturas y normalizar evidencia histórica de forma explícita. Añadir CLI SEO, QA y reportes sin score único.
5. Evaluar MCP por mantenedor, versión, permisos y superficie. Implementar adaptadores desacoplados con transporte inyectable/importación offline, allowlist de propiedades/dominios, límites, errores y desconexión. No instalar ni conectar cuentas.
6. Pruebas unitarias/integración/browser y ocho evaluaciones SEO basadas en acciones/evidencia, más regresión de V2. Conservar hashes de origen y documentos importantes; registrar pendientes reales.

Se aceptan capacidades por casos ejecutados y artefactos. GSC/GA/Merchant reales, RRT y Schema Validator no se darán por consultados sin hacerlo. HTML y JSON válidos no prueban indexación, resultados enriquecidos, tráfico o causalidad. Los adaptadores simulados no acreditan conexiones reales.
