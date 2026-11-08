# Reutilización entre tiendas

El [catálogo](catalog.json) distingue conocimiento (A), patrones (B), procedimientos (C), código con autorización comprobada (D), código exclusivo del cliente (E), funcionalidad nativa (F) y recursos sin derecho de redistribución comprobado (G). No hay entradas D/E/G de código de clientes: no se recibió autorización para distribuirlo. Los contratos JSON describen interfaces observadas y no incluyen implementaciones del tema.

Para una nueva tienda registra el proyecto y su adaptación local; busca el componente nativo, compara versión/hash y configura branding en los tokens/settings existentes. La [estrategia original multitienda](../ipanema-discovery/08-design-system/multi-store-strategy.md) sigue siendo la fuente arquitectónica. Ipanema no adquiere por este catálogo una función de importar bibliotecas arbitrarias en el editor.

Los [contratos](contracts/native-commerce.json) y el [helper de imagen](contracts/native-image.json) tienen versión semántica propia y versión de tema observada. Un cambio de parámetro, selector o evento incompatible exige nueva versión mayor del contrato y prueba de todos sus consumidores. No actualizar 20 tiendas en lote solo porque el cambio pase en una; registrar compatibilidad por proyecto/versión en los reportes QA.

Los tokens visuales y su distribución se mantienen en [tokens del discovery](../ipanema-discovery/08-design-system/tokens.md). Sus valores no se convierten en defaults de todas las tiendas. El adaptador de cada proyecto usa settings/tokens actuales del tema y conserva branding local; no se crea una segunda hoja global de overrides.

## Soluciones con evidencia

Hallazgo: observación con fuente/fecha en findings.json. Propuesta: recomendación aún sin validación. Solución verificada: archivos y resultados respaldados por una ejecución QA pertinente. `python3 tools/ia.py solutions` calcula su vigencia; si cambian fuente, evidencia, versión del agente o proyecto, exige revalidación. No modifica automáticamente las conclusiones históricas.

Registrar una solución:

```bash
python3 tools/ia.py solutions --register /ruta/entrada.json --evidence /ruta/al/reporte-qa.json
```

La entrada requiere id, problem, context, component, files (rutas relativas), cause, solution, tests, results, limitations, risks, compatibility, reuse y scope (`workspace` o `theme`). El registro agrega fecha, versión, proyecto, hashes y evidencia. Un reporte genérico no demuestra pertinencia: el agente debe comprobar que las pruebas cubren ese cambio y explicar el límite. No convertir una recomendación en regla universal ni usar una respuesta del chat como prueba ejecutada.

La distribución de código propio necesita una licencia/permiso explícito antes de publicarse fuera del proyecto. El repositorio no contiene un dictamen de derechos del tema. Se comparten procedimientos y contratos; una sincronización o publicación de tiendas requiere autorización específica.
