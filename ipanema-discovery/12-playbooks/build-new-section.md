# Modificar o crear una sección sin duplicar

Flujo para una petición futura de implementación. Durante discovery se documenta, no se instala código.

1. Convertir el pedido visual en contenido, layout e interacción. Determinar si debe cambiar una instancia o todas. Usar `tools/find_component.py` y seguir callers; comprobar source actual y settings reales.
2. Probar primero la composición existente: hero/banners, rich-text/group, image/text, products, FAQ y controles responsive. Una combinación nueva no implica un tipo nuevo. El bloque code es una extensión posible, no el lugar por defecto para reimplementar componentes.
3. Si hace falta un tipo nuevo, explicar qué falta en lo nativo y qué consumidores compartirían su lógica. Comprobar fork remoto y permisos del cambio; en este proyecto ya se observó fork, pero ese dato debe revalidarse en la siguiente tarea.
4. Preparar un diff local mínimo. Reutilizar image.tpl, icon.tpl, botones, formularios y comercio. Schema con ajustes necesarios, traducciones en archivos existentes y presets que no copien datos de otras tiendas. Mantener block_attributes y contratos del editor; no mezclar Liquid de Shopify con Twig.
5. Un solo contenido para dispositivos. Usar tokens y clases de componente, reservar medios y evitar layout diferido a JS. No añadir !important sin un conflicto de cascada demostrado.
6. Si requiere JS, integrarlo en la inicialización existente por instancia, sin otro motor ni listeners repetidos. Mantener fallback y cleanup. No replicar precio, stock, variantes o carrito.
7. Comparar HTML inicial/cargado, teclado, red, seis anchos y estados aplicables. Medir delta de assets, recursos ocultos y shifts. Ejecutar solo checks relevantes, sin instalar un ecosistema de tests por un cambio de espaciado.
8. Entregar qué se reutilizó, diff, validación, coste, límites y estrategia de actualización. Revisar el diff remoto incluido borrado antes de enviar. No publicar por el simple hecho de que el diseño se vea bien.

Fuentes de decisión: [inventario](../02-native-components/component-inventory.md), [configuraciones](../02-native-components/settings-matrix.md), [arquitectura reusable](../08-design-system/component-architecture.md).
