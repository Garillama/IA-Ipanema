# CLI instalado y flujo comprobado

Fecha: 2026-11-08. Ejecutable detectado: `/home/alanrichard/.local/bin/tiendanube`, **2.5.1**. Los paquetes existentes incluyen Puppeteer, Lighthouse y axe-core, usados desde scripts de auditoría; no se instalaron dependencias.

| Comprobación ejecutada | Resultado |
|---|---|
| --version y theme --help | Versión y comandos disponibles registrados por inspección local |
| theme preview | Generó URL de lectura para 14837617; no abrió watch ni publicó |
| theme diff --json | forked true, in_sync true, 329 iguales, sin eliminaciones ni fallas |
| theme list --json | Ipanema Deco 1.8.0, is_productive true, fork true; registro filtrado sin credenciales |
| theme performance --help | Existe comando de Lighthouse; las mediciones se ejecutaron con el paquete instalado desde esta carpeta |

No se ejecutaron pull/push/watch/fork/unfork/update/publish/check ni operaciones FTP. `theme check` existe, pero no se reporta como validación ejecutada. Tampoco se ejecutó renderizado Twig local: el servidor de Tiendanube renderizó las páginas.

El installed help conserva `theme authorize`; documentación reciente describe también credenciales por alias/auth. Verificar `--help` de la versión que se vaya a usar; no pegar comandos de una skill antigua como si fueran universales. La [guía oficial de desarrollo](https://tiendanube.dev/themes/developer-tools/cli/sectionable-theme-development) y el comportamiento observado son las referencias para una tarea futura.

Para preparar un cambio, confirmar tienda/tema, preservar datos locales y del comerciante, revisar un diff completo y validar lo que realmente se enviaría. Push sincroniza también eliminaciones; watch puede enviarlas al guardar. No copiar esta base de documentación dentro de una raíz de tema y ejecutar push desde ahí. El repositorio del agente es un directorio separado precisamente para evitar ese error.

Un exit code 0 de diff no significa ausencia de diferencias: leer in_sync y summary. Un manifiesto puede quedar viejo aunque los archivos estén sincronizados. La identidad remota se registra por operación y fecha, no como permiso permanente para escribir.
