# Eventos, símbolos y puntos de extensión encontrados

Fecha: 2026-11-08. Método: lectura/búsqueda estática en store.js, layout y snippets. No es una lista exhaustiva de eventos públicos de Tiendanube.

| Contrato | Fuente local | Interpretación |
|---|---|---|
| LS.ready | layout.tpl L122 | Ordena carga de librerías dependientes y store.js |
| cart.updated | store.js L3585 | Evento DOM usado por favicon; distinto de cart:update del SDK |
| shipping.options.checked | store.js L3396 | Actualiza estado de shipping/totales en el tema |
| brand-editor:select-element | store.js L3925 | Tipo de postMessage desde parent; no endpoint ni evento DOM universal |
| js-* / data-store / data-component | Templates y snippets | Contratos de motor, editor y apps; preservar consumidores |
| section id / block_attributes | Schemas y wrappers emitidos | Identidad de instancia para editor, no nombre portable de componente |

LS consumidos en source: addToCartEnhanced, asyncCart, calculateShippingAjax, changeQuantity, changeVariant, fillCrossSelling, fillQuickshop, formatToCurrency, freeShippingProgress, homePopup, hybridScroll, loadVideo, minusQuantity, newsletter, plusQuantity, productItemSlider, registerOnChangeVariant, removeItem, resolveVariantsCarrierElement, saveCalculatedShipping, subscriptionChangeVariant, subscriptionSubmit, updateNotificationDiscountLabel y updateShippingProduct; además currency, ShippingDiscountRow y addToTotal. Su aparición demuestra uso por el tema, no documentación como API estable para aplicaciones externas.

Los listeners nativos incluyen click/change/submit, keydown/keypress, focusout, pointerdown, mouseenter/leave, load, message, resize/scroll, transitionend y visibilitychange. El coste depende de lo que ejecutan y cuántas veces se registran. Las fichas enlazan líneas donde cada hook aparece en store.js.

initPreviewMessageListener valida event.source contra window.parent y tipo de payload; no usa origen como único filtro por srcdoc. Vídeos también usan postMessage y listeners temporales. Una modificación debe conservar validación y evitar listeners acumulados. No llamar manualmente rutas internas inferidas de comentarios como una API de integración soportada.
