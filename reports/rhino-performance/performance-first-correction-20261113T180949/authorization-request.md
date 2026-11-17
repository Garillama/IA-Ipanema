# Solicitud específica — todavía no autorizada

Solicitamos autorización para publicar exclusivamente `sections/google-reviews.tpl` en la instalación publicada14828608, tienda7400935, mediante un solo upsert nativo sin eliminaciones.

Parche SHA256 `2c88fb0d3e619b5d08c8e217eecb9e104d9d402dbe47997c95b91f0e4b1c8d32`.

Preimagen obligatoria `75a487600c5d71001fa2e0970dad1cb943f80d399f1af89db559bffc3253fd30`.

Postimagen obligatoria `e6f79c2fd59376efe955662adff44d13329300360a118249c88480d59dde3cd3`.

Incluye reconfirmación GET de instalación/hashes, verificación del respaldo existente, un único PATCH exacto de ese archivo y comprobación GET posterior. Ante cualquier diferencia o cambio ajeno, detener. No se autoriza sincronización global ni otros archivos.

Solicitamos por separado dentro de la misma decisión el alcance de QA posterior descrito en QA-AND-ROLLBACK.md: Home en seis anchos y cinco Lighthouse por dispositivo, solo lectura, POST/formularios/compras bloqueados, sin GSC/PSI/CrUX ni configuración remota de apps. Sin ese alcance no se ejecutarán nuevas mediciones.

Si se acepta reversión controlada: únicamente este archivo ante una regresión crítica atribuible y con hash remoto igual a la postimagen aprobada; restaurar respaldo y verificar hash, sin sobrescribir cambios posteriores. La mera autorización de publicar no se interpreta automáticamente como permiso de reversión.

El propietario debe aceptar los riesgos y límites descritos en README.md. La validación autorizada ya terminó sin publicación; esta solicitud no habilita ninguna operación hasta recibir respuesta específica.
