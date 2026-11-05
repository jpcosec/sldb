REFORMULACION
PK03 es un paquete de planificación (`aggregate`) del repo sldb; no se ejecuta: cierra cuando cierran sus hijos GO06 y GO07. Su propósito es incorporar a sldb reglas como documentos y anclas a documentos con hash de contrato. El resultado sustantivo es: `RuleDoc` y `rules check/explain` (GO06), y anclas `doc:` con pinneado, estados `intact/changed/lost`, `anchors check` y `anchor_state` consultable desde reglas (GO07). Límites: no define modelos de recibo, no autentica actores, no produce hechos externos, no persiste hechos derivados y no cambia el lenguaje ni el shard para `anchor_state`.

AMBIGUEDADES
Ninguna.

DRY-RUN
Hipotéticamente, GO06 se ejecutaría tras GO05: leería el parser/semántica de GO05, GO02, el registro de modelos y `base_models`, `Finding` y el envelope CLI; produciría el modelo `RuleDoc`, `api/rules/`, comandos `rules check/explain`, validación al escribir, findings con cláusula y documentación. Transferiría a GO07 la superficie de reglas y evaluación necesaria para probar `anchor_state`.

GO07 se ejecutaría tras GO04 y GO05; para su aceptación basada en una regla, requiere además la salida de GO06, aunque no haya arista explícita entre hermanos. Leería la proyección y `field_hashes` de GO04, el lenguaje de GO05, `Provenance`, los pasos de guardado y el índice de aristas. Produciría parseo/validación de `doc:`, pinneado, estados, `check_doc_anchors`, extensión de `anchors check`, entrada derivada `<campo>__anchor_state` y documentación. Transferiría al resultado conjunto un `anchor_state` consultable por reglas.

Validación conjunta futura: store temporal con jerarquía de modelos; `RuleDoc` con sujeto `model <= X`; documento A con `subject` anclado a B; editar contrato de B → `changed`, editar fuera del contrato → `intact`, borrar B → `lost`; `anchors check` reporta alertas; la regla `any(^subject: anchor_state = "intact" and verdict = "accepted")` evalúa true/false según corresponda; valores no `doc:` rechazados; tests, docs y CHANGELOG.

FUTURO
GO05 y GO04 deben entregar lenguaje y proyección; el gate `G_SEMANTICS` debe estar resuelto. GO08 cablea `stores check`; GO10 retira shims; un humano escribe la disposición de esta revisión. El TaskDoc fijará nombres exactos de archivos y tests. La prueba de consumo y `G_CONSUMER` pertenecen al plan de deskops. D5–D8 ya están decididas.
