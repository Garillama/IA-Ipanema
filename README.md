# Agente cotidiano para Ipanema

Esta carpeta prepara al asistente que abras aquí para investigar y mantener Tiendanube con las reglas de [AGENTS.md](AGENTS.md), una [skill local](.agents/skills/ipanema-storefront/SKILL.md), herramientas de lectura y una [base de conocimiento](ipanema-discovery/README.md). La configuración por carpeta y las skills siguen los mecanismos de la [documentación oficial de OpenAI](https://developers.openai.com/codex/guides/agents-md).

Puedes pedir, por ejemplo: «Analiza cómo cambiar este hero usando los controles existentes», «Prepara una variante mobile sin duplicar contenido» o «Revisa la product card y sus consumidores antes de editarla». La primera entrega es discovery; no se modificó el tema. Una futura petición de implementación define el alcance del trabajo local; publicar o sincronizar la tienda requiere instrucciones aplicables.

El proyecto inicial se encuentra en [projects/ipanema.json](projects/ipanema.json). Se comprobó sincronización remota y acceso autorizado al storefront Ipanema 1.8.0. Se recorrieron 48 URLs y 13 tipos públicos en seis anchos representativos. La pantalla de contraseña sin sesión entrega recursos de otra instalación y se documenta aparte. Consulta el [informe de cobertura](ipanema-discovery/DISCOVERY-COMPLETENESS-REPORT.md) para los estados y superficies que siguen pendientes.

```bash
python3 tools/find_component.py "producto"
python3 tools/find_component.py "hero"
python3 tools/check_workspace.py
```

Para una nueva captura estática usa un destino de evidencia nuevo, fuera del tema:

```bash
python3 tools/audit_source.py --source /ruta/autorizada/del/tema --output /ruta/fuera-del-tema/evidencia-fechada
```

Los scripts no instalan dependencias. Las auditorías de navegador ya ejecutadas usan Chrome y paquetes existentes del CLI de Tiendanube. No hay servicio en segundo plano ni automatización que publique al guardar.

Se revisó [Craft Anything](https://github.com/storytold/craft-anything) y se adoptó su enfoque de investigación con evidencia y verificación: [evaluación y alcance](ipanema-discovery/01-architecture/craft-anything-assessment.md). No se copió su aplicación Rust ni código del tema a una biblioteca. El ejecutable Craft Anything no está instalado en este entorno.
