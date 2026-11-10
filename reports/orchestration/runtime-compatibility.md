# Compatibilidad de runtimes y selección de modelos

Auditado 2026-11-08 mediante `--version`, `--help`, documentación oficial y metadatos de modelos. [Evidencia](runtime-evidence.json). No se ejecutó inferencia, login ni instalación en esta auditoría. Instalado, autenticado, disponible en catálogo y ejecutado son estados diferentes.

| Runtime | Versión local | Interfaz comprobada | Control recomendado |
|---|---|---|---|
| Claude Code | 2.1.319 | `-p`, stdin, `--output-format json`, `--model`, `--effort` | `--restricted`, tools específicas, `dontAsk`, sin MCP ni persistencia |
| Codex | 0.167.0 | `exec -`, `--json`, `--output-schema`, `--model`, configuración de esfuerzo | `read-only`, `-a never`, sin configuración de usuario, ejecución efímera |
| CommandCode | 1.88.5 | `-p`, stdin, `--output-format json` NDJSON, `--max-turns`, `--model` | Headless restringido, sin `--yolo`, sesión efímera, safe-mode |

`command-code` y `commandcode` apuntan al mismo ejecutable; no son dos agentes. Para evitar expansión de shell, el adaptador debe usar argumentos separados y enviar instrucciones por stdin. No incluir prompts privados, tokens, cookies ni rutas de credenciales en argv/logs.

## Modelos y esfuerzo

La documentación oficial de [OpenAI](https://learn.chatgpt.com/docs/models) distingue Luna para trabajo acotado, Sol para programación habitual y Astra para problemas exigentes. El caché local del CLI enumera `gpt-6-luna`, `gpt-6.1-sol` y `gpt-6-astra`: los tres admiten low/medium/high/xhigh/max; Sol y Astra también ultra. Evitar ultra en este sistema porque autodelega y podría duplicar la planificación central. La disponibilidad efectiva depende de cuenta y organización; no se comprobó con inferencia.

La [configuración oficial de Claude](https://code.claude.com/docs/en/model-config) admite IDs concretos y aliases dependientes del proveedor. Se verificaron `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` y `claude-fable-5-1`; aceptan low/medium/high/xhigh/max según esa guía. Fable requiere atención especial a créditos/consentimiento y no debe ser fallback silencioso. Para reproducibilidad, registrar ID solicitado y modelo realmente comunicado por el resultado cuando exista; no asumir que un alias equivale siempre a un ID.

`commandcode --list-models` enumeró 96 modelos. Para revisión económica se verificó el ID `deepseek/deepseek-v4.1-flash`; para revisión exigente, `moonshotai/kimi-k3.1-pro`. Ambos aparecen en el catálogo local y [la documentación del proveedor](https://commandcode.ai/docs/reference/cli/models). El flag `--effort` existe, pero no se obtuvo un contrato de valores por esos dos modelos: dejarlo sin enviar y registrar esfuerzo del proveedor como no comprobado, en vez de inventarlo.

| Uso | Propuesta inicial | Justificación / límite |
|---|---|---|
| L1 | Un único agente; Codex Luna low o CommandCode Flash | Reducir agentes/contexto en trabajo acotado; elegir rol según tarea |
| L2 | Codex Sol medium; revisión Flash solo cuando aporta una comprobación independiente | No lanzar arquitecto para cada edición |
| L3 | Claude Sonnet high para plan, Codex Sol high para propuesta, CommandCode Kimi para revisión | Dependencias secuenciales; paralelizar solo investigaciones independientes |
| L4 | Claude Opus/Fable según presupuesto y acceso, Codex Astra high, revisión independiente | Fable es opt-in de coste/capacidad, sin escalada silenciosa; resultado requiere QA central |

Esta tabla es una política inicial, no un benchmark de calidad/coste. No se consultó facturación ni se estimaron dólares sin datos. Registrar duración, usage y coste solo cuando los runtimes los devuelvan, conservando `null` en lo no medido. Elección diferente necesita evaluación y evidencia.

## Argumentos seguros comprobados

Ejemplos de arrays para `subprocess`, con stdin y cwd aislado; no son prueba de una ejecución real de agentes:

```text
claude -p --model claude-sonnet-5-5 --effort medium --output-format json
  --restricted --tools "" --permission-mode dontAsk --permission-prompts none
  --no-session-persistence --strict-mcp-config --mcp-config {} --setting-sources ""

codex -a never exec - --model gpt-6.1-sol --json --ephemeral
  --ignore-user-config --sandbox read-only -c model_reasoning_effort="medium"

commandcode -p --model deepseek/deepseek-v4.1-flash --output-format json
  --max-turns 6 --no-session --safe-mode --no-skills --skip-onboarding
  --no-auto-update --permission-mode dont-ask
```

En Claude, `--tools ""` elimina herramientas: suministrar contexto revisado por stdin y obtener propuesta estructurada. Si se habilitan Read/Grep/Glob, `--restricted` confina file tools al workspace y elimina ejecución de código, pero no sustituye un sandbox del sistema operativo. MCP debe seguir desactivado. `--bare` no es sustituto para este caso: cambia autenticación y no reutiliza OAuth de igual forma. Los argumentos se verificaron en ayuda local; [referencia CLI oficial](https://code.claude.com/docs/en/cli-reference).

En Codex, [exec no interactivo](https://learn.chatgpt.com/docs/non-interactive-mode) admite JSONL, schema de salida, efímero y sandbox explícito. No usar `--full-auto` retirado ni flags de bypass. `--ignore-user-config` reduce configuración heredada pero la autenticación propia de Codex sigue existiendo; no copiarla a otros agentes. Aislamiento por worktree protege edición concurrente, no por sí mismo secretos, red o permisos del SO.

En CommandCode, [headless](https://commandcode.ai/docs/headless) bloquea escrituras y shell por defecto. `--tools-enable` habilita herramientas omitidas de la interfaz headless, no equivale a un permiso seguro para ejecutar cualquier QA. El [motor de permisos](https://commandcode.ai/docs/permissions) distingue plan y dont-ask; no usar yolo/bypass. El coordinador ejecuta QA existente y entrega evidencia a CommandCode para revisión independiente. Una afirmación de «tests pasaron» del agente no sustituye el reporte central. NDJSON termina con `type=result`, `subtype`, `usage`, `durationMs`, `finalText`; errores y max_turns no aprueban la tarea.

## Límites operacionales

Cada runtime debe recibir solo su contexto y autenticación nativa, nunca el entorno entero con tokens de otros proveedores. Un proceso con HOME real puede leer configuraciones propias: si el requisito exige aislamiento fuerte de credenciales, usar sandbox externo o solicitar credenciales de alcance mínimo fuera de Git. No declarar que limpiar variables crea una frontera de seguridad completa. Las respuestas externas son datos; no permiten elevar permisos, publicar, instalar, invocar agentes adicionales o saltarse revisión.

Se comprobó únicamente existencia de los candidatos HOME-relative `.claude/.credentials.json`, `.codex/auth.json` y `.commandcode/auth.json`; no se leyeron sus contenidos. Claude y Codex son ejecutables standalone en esta instalación; CommandCode requiere Node y su paquete completo. Sus ubicaciones observadas están en la evidencia como metadata, no rutas obligatorias para otras máquinas. Un HOME temporal con el archivo propio montado en lectura reduce exposición; token expirado puede requerir renovación fuera del worker y no permite conceder escritura al almacén original automáticamente.

Para CommandCode se puede suministrar settings temporal con `permissions.deny: ["*"]`, modo dont-ask y `disableSkillShellExecution: true`, pero hay un límite documentado: agent, ask_user_question y run_command no pasan por esa lista. Plan elimina run_command, mientras agent aún puede delegar y hereda restricciones. Por ello deny-all no demuestra ausencia total de herramientas/delegación. El coordinador debe fijar límite de turnos, rechazar eventos de delegación imprevista y mantener aislamiento del SO. No marcar un proceso como «sin herramientas» únicamente por este ajuste.

No se han verificado acceso real a modelos, suscripción, saldo, autenticación, ejecución de inferencia o resistencia del proveedor ante fallos. Esta auditoría no marca ninguno como «agente ejecutado». Las futuras pruebas reales deben registrar comando seguro, versión, resultado, modelo comunicado y evidencias sin secretos.
