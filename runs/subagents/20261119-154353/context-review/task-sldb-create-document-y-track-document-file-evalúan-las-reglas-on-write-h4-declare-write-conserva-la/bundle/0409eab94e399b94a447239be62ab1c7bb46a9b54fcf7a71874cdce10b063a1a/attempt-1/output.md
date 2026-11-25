REFORMULACION
Propósito: cerrar H4–H7 de GD27 en sldb. Resultado: `create_document` y `track_document_file` evalúan `on_write`; `stores declare --write` conserva `tag_namespaces`/`tag_models`; la familia de tags expone evaluación estructurada en JSON; docs declaran qué documentos ve. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: superficies listadas (api/documents, rules, tags, stores, cli/commands, tests, docs, CHANGELOG, `contracts/layers.toml`); fuera borrar el puente de deskops, que `stores build` evalúe `on_write` y cambiar qué reglas existen. Es ejecutable, no agregado.

AMBIGUEDADES
1. H6 choca con el contrato: task «el hallazgo ... lleva su evaluación estructurada ... como dato propio»; `rules.md` «`Finding` no gana campos.» Obliga a inventar dónde vive el dato y el esquema JSON.
2. Docs ya describen H4/H6/H7: `tags.md` «### Which documents the family sees (H7)» y «`{"findings": [...], "evaluations": [...]}` (H6)»; `rules.md` «Alta de un documento (H4). `create_document` y `track_document_file` corren este mismo paso». Obliga a decidir si son especificación objetivo o trabajo ya hecho, y si q4 es no-op.
3. Origen retirado: «retirado en el triaje 2026-11-16» vs «el ítem de drawer de origen se dan de baja por CLI al cierre». Obliga a inventar si el cierre retira algo inexistente.
4. q1 abierto: «El worker revisa si StoreDeclaration tiene otra clave autorada que declare --write pierda, y la suma si la hay». Obliga a inventar el universo de claves y el criterio.
5. «una declaración con tags regenerada por `stores declare --write` queda igual». Obliga a inventar igualdad: bytes vs parseo, orden, comentarios.
6. «Los 7 pasos del workflow de sldb los corre el coordinador» vs validación «7 pasos del workflow de sldb en clon limpio». Obliga a inventar quién ejecuta y atestigua.

DRY-RUN
Lecturas: task, rituales, `rules.md`, `tags.md`, `layers.toml`; luego código citado (`rules_on_write.py`, `payload_save_steps.py`, declare, `builtin_tag_rules.py`, `tag_check`/`rules_check`/`rules_explain`) y tests. Cambios previstos: q1 declare_store; q2 llamada a `check_on_write` en create/track; q3 dato estructurado y salida JSON; q4 docs; q5 tests. Dependencias: API de stores, declaración, capas, findings. Validaciones futuras: tests por H, `test_clean_code_rules`, `tools/check.sh --fast`, suite por archivo desde `/dev/shm`, 7 pasos en clon limpio. Sin ejecutar.

FUTURO
Otro nodo implementa y corre tests; el coordinador corre los 7 pasos y decide las ambigüedades 1–6; deskops retira su puente cuando esta tarea entre.
