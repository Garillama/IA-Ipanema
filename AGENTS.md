# Agente de ingeniería de tiendas Tiendanube

Trabaja en español. Este directorio es el centro de conocimiento y herramientas; el tema de la tienda vive en otra ruta. Selecciona el proyecto en `projects/ipanema.json` y confirma ruta, instalación y generación del tema antes de actuar.

Para tareas Ipanema usa `.agents/skills/ipanema-storefront/SKILL.md`. Lee primero `ipanema-discovery/00-executive-summary.md`, el informe de cobertura y solo los documentos del componente afectado. La evidencia es fechada: vuelve a verificar el archivo y el estado remoto cuando una decisión dependa de ellos.

## Reglas de trabajo

- Durante un discovery, cambia únicamente documentación y herramientas de auditoría de esta carpeta. No modifiques el tema, configuraciones, catálogo, carrito, apps o publicación.
- Una petición posterior de implementación autoriza el trabajo local reversible necesario dentro de su alcance. Antes de editar, identifica el componente que ya existe, sus consumidores y las configuraciones disponibles. Conserva cambios ajenos y resuelve conflictos concretos; no hagas stash, pull ni descartes automáticos.
- Reutiliza configuración nativa, tokens, snippets y motores existentes. Cambia la fuente del componente antes de añadir otra implementación u overrides acumulados. Diferencia cambio global y variante por instancia.
- No añadas `!important` por defecto. Una excepción necesita explicar el conflicto real de cascada, tener selector acotado y verificación. No borres los `!important` utilitarios nativos indiscriminadamente.
- El layout básico debe salir correcto del HTML y CSS iniciales. No ocultes la tienda hasta que JS la rediseñe. Evita dos copias del mismo contenido para desktop/mobile; usa el layout responsive y conserva orden de lectura.
- Mantén contratos de comercio, `data-store`, `js-*`, atributos del editor y slots. No reproduzcas lógica de precio, stock, variantes, carrito o envíos.
- Verifica el tema remoto: este discovery encontró un manifiesto local desactualizado, y una página de contraseña que entrega assets de otra instalación. Un URL solicitado, Git limpio o `manifest.json` aislado no prueban qué tema se renderizó.
- No ejecutes `watch`, `push`, `publish`, `fork`, `unfork`, `update`, `pull`, instalaciones o cambios remotos sin autorización aplicable. `watch` sube al guardar. Antes de enviar, revisa el diff completo, incluidas eliminaciones; publica únicamente con instrucciones explícitas y revisión concreta.
- No leas ni copies tokens a evidencias. `.nuvem`, archivos de entorno y sesiones no pertenecen a la base de conocimiento. Usa el CLI instalado para lecturas autorizadas.
- No copies código del tema a otras tiendas sin permisos comprobados. Los patrones y contratos documentados no transfieren licencias.
- Presenta cada conclusión como confirmada, inferida, no comprobada o no disponible. Nunca declares métricas, accesibilidad AA, SEO o cobertura total sin pruebas ejecutadas del mismo contexto.

## Entrega de cada tarea

Explica componente reutilizado, archivos afectados, motivo, comprobaciones ejecutadas y límites. Actualiza el hallazgo o playbook principal, sin duplicarlo. Si algo no pudo probarse, registra exactamente qué faltó. No añadas bibliotecas ni pruebas que no ayuden a verificar el cambio.
