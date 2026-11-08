# Estrategia para varias tiendas

Fecha: 2026-11-08. Propuesta basada en archivos y CLI reales; no existe una biblioteca compartida implementada ni se verificó importación de paquetes arbitrarios en Brand Editor.

Se pueden compartir metodología, criterios, contratos, esquemas propios y patrones. Compartir implementación del tema exige derechos de uso y compatibilidad de versión. Los valores de marca, catálogo, medios, templates y settings de cada comerciante deben permanecer por tienda. Un @media-lib o menú de una tienda no es portable por copiar su referencia.

| Mecanismo | Uso viable | Coste / limitación |
|---|---|---|
| Tipos nativos + configuración por tienda | Personalización sin otra lógica de comercio | Disponibilidad varía por versión; datos no son automáticamente portables |
| Templates/presets propios | Variantes de composición revisadas | Normalizar referencias a medios/productos/menús; respetar asignación y límites del editor |
| Código propio distribuido en repositorio | Versionar módulos y preparar cambios revisables para forks autorizados | No es npm ejecutándose en storefront; necesita integración con archivos del tema y QA |
| Migraciones/patches por versión | Reaplicar una mejora con precondiciones y diff | Fallar ante contexto distinto; nunca reemplazar masivamente datos de tiendas |
| App Nube SDK | Funcionalidad compartida en slots y eventos soportados | Infraestructura/permisos y límites de superficie; no acceso arbitrario al theme DOM |

Propuesta de versionado: contrato del módulo con versión, rango de Ipanema validado, dependencias y cambios incompatibles; releases con ejemplos de configuración y comprobaciones. Un cambio de hook, schema, nombre de setting, evento, markup comercial o token puede ser breaking aunque el aspecto parezca igual. La versión de la base y la de personalizaciones deben registrarse por separado.

Para veinte tiendas, mantener una matriz instalación→versión→fork→módulos→estado de QA. Preparar diffs específicos contra cada instalación y conservar las elecciones del comerciante. La actualización de base debe revisarse antes de distribuir mejoras: no convertir un fix local en reemplazo automático de todos los temas.

Después de doce meses, los principales riesgos son forks divergentes, scripts de apps duplicados, referencias de medios inválidas, tokens por tienda sin trazabilidad y pruebas basadas en una sola home. La base aquí evita repetir discovery, pero no elimina la verificación de estado remoto ni concede licencias de redistribución.
