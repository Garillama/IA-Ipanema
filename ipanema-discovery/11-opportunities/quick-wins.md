# Cambios pequeños que conviene evaluar primero

Propuestas, no cambios ejecutados. Fecha: 2026-11-08. La facilidad no reemplaza severidad; consultar [prioridades](priority-matrix.md).

| Oportunidad | Beneficio | Coste y condición |
|---|---|---|
| Identificar instalación y corregir metadatos en flujo autorizado — IPN-001/002 | Evita trabajar en contexto equivocado | Lectura barata; no usar pull para arreglarlo sin preservar datos |
| Ajustar flechas del carrusel — IPN-004 | Quita overflow intermedio | CSS acotado y QA de todos sus consumidores |
| Corregir contraste editorial de instancia — IPN-006 | Mejora lectura | Verificar colores/estados sin alterar otras secciones |
| Revisar H1 del contenido importado — IPN-007 | Jerarquía más clara | Necesita decisión/editorial del catálogo; no modificar durante discovery |
| Evitar segunda card/helper — IPN-003 | Reduce mantenimiento y código | Usar composición/variante existente antes de desarrollar |
| Asegurar lista JSON-LD vacía válida — IPN-017 | Corrige sintaxis de 404 | Cambio compartido con prueba de ramas y sin añadir otro schema |

Menú accesible e indexación de paginación tienen alto valor aunque requieran más análisis/regresión que un ajuste visual. No desplazarlos por tareas más fáciles solo para cerrar más ítems.
