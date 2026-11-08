---
name: ipanema-storefront
description: Investigar y mantener temas seccionables Ipanema de Tiendanube, reutilizando sus secciones, bloques y lógica de comercio con controles de rendimiento, SEO y responsive. Usar en esta carpeta para discovery o cambios de temas Ipanema; no aplicar reglas de este modelo a temas clásicos o Shopify.
---

# Ipanema Storefront

La raíz de trabajo de esta skill es `../../..` desde su carpeta. El tema se selecciona en `projects/ipanema.json`; no está dentro de esta skill. Revisa `AGENTS.md`, `ipanema-discovery/00-executive-summary.md` y `ipanema-discovery/DISCOVERY-COMPLETENESS-REPORT.md` antes de usar conclusiones anteriores.

## Descubrir lo que ya existe

Confirma `.tpl` con schema, `sections/`, `blocks/`, `snippets/` y `templates/pages/*.json`. Busca con `python3 tools/find_component.py "consulta"` y sigue los consumidores en el grafo. Comprueba el archivo actual: las fichas son evidencia estática fechada, no una garantía del estado remoto.

Prioriza settings y composición nativos. Lee el playbook correspondiente de `ipanema-discovery/12-playbooks/` solo si la tarea lo requiere. Para tarjetas, PDP, carrito y carruseles consulta `07-commerce/`; para imágenes `05-performance/image-loading.md`; para cascada y dispositivos `03-editor/responsive-controls.md`. El inventario completo y los defaults están en `02-native-components/`.

## Elegir el cambio

Define si el pedido afecta a todas las instancias o solo a una. Usa tokens globales para identidad compartida y configuración de instancia para variantes. No crees un segundo motor de carrusel, componente de imagen, modal o formulario de compra cuando el existente cubre el caso. No uses JS para corregir un layout que puede renderizarse con CSS. Los hooks LS del tema no se convierten por eso en una API pública para integraciones.

La fase discovery solo genera conocimiento, evidencia y herramientas aquí. En una implementación posterior, prepara un diff local revisable dentro de la autorización recibida. Antes de tocar archivos de datos verifica sincronización y cambios del comerciante; no ejecutes pull automático. El estado de fork y versión debe contrastarse con una lectura remota autorizada; un manifiesto puede estar viejo. Los datos del editor sobreviven de forma distinta al código de un fork: consulta `01-architecture/platform-limitations.md`.

## Verificar el resultado

Compara HTML inicial, layout antes y después de JS, seis anchos y estados relevantes. Comprueba `currentSrc` y red para imágenes; DOM no equivale a descarga. No certifiques home/PDP si la navegación terminó en `/password/`. Mantén enlaces rastreables y evita duplicar meta tags y JSON-LD existentes. Motion debe conservar contenido disponible y respetar movimiento reducido.

Las herramientas en `tools/` leen el origen y escriben evidencia en otra carpeta. Reutiliza paquetes ya instalados; los scripts de navegador de este entorno resuelven Puppeteer, axe y Lighthouse desde el CLI de Tiendanube. Si faltan, registra el límite antes de proponer una instalación. Ejecuta `python3 tools/check_workspace.py` para validar enlaces, integridad del origen y consistencia del inventario; no sustituye QA del storefront.

Entrega qué se reutilizó, el diff, los resultados reales y pendientes. Actualiza la fuente principal del tema investigado y el registro de correcciones si aparece evidencia que contradice una conclusión.
