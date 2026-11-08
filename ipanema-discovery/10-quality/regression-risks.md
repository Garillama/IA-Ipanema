# Riesgos de regresión

Fecha: 2026-11-08. Matriz derivada de dependencias encontradas y comportamiento observado.

| Cambio | Qué puede romper | Prueba necesaria |
|---|---|---|
| Helper image | Hero, banners, cards, galería, logos, placeholders | Prioridad, art direction, sizes, ratios, red y sin JS en todos los callers afectados |
| Card común | Home, categoría, búsqueda, carruseles, relacionados | Modos reduced/slide, variantes, promociones, JSON-LD y datos duplicados |
| Modal compartido | Menú, quick shop, carrito, filtros, notificaciones | Foco, teclado, nombre, Escape, scroll lock y retorno al disparador |
| Breakpoint md | Header, cards, galería, motor JS y utilidades | 767/768/769, seis anchos y resize/orientación |
| CSS global/tokens | Todas las páginas y contenido del comerciante | Contraste, medidas, fuentes y layout inicial/cargado |
| Payload de variantes | Cards y PDP, kits/suscripciones | URL inicial, disponibilidad, precio y stock sin replicar lógica |
| Inicialización | Brand Editor, contenido dinámico, carga incremental | Repetir ciclos; listeners/observers/timers y duplicados |
| Hooks data-store/slots | Apps y analytics | Revisar contratos antes de renombrar/eliminar |
| JSON/valores del editor | Preferencias del comerciante y asignación de templates | Diff de estado remoto y reconciliación explícita |
| Actualizar fork | Código propio y contrato del release | Comparar base, cambios locales y migración; QA en borrador autorizado |

No hacer un refactor global por un fix de una sola instancia. Tampoco copiar el componente completo para evitar revisar su alcance. Usar la variante mínima que represente el requisito y comprobar consumidores reales.

Antes de publicar, una reversión debe estar definida por cambios concretos y respaldos verificables. Esta investigación no ejecutó publicación ni garantiza rollback automático de Tiendanube.
