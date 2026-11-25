## REFORMULACION

Encargo: ejecutar la tarea de código GD27 en el repo `sldb`, en un worktree de robocop2 separado de grafo-operable. Propósito: generalizar desde deskops espacios de nombres y jerarquía de tags, y reemplazo de texto en documentos trackeados. Resultado: `StoreDeclaration.tag_namespaces` con validación por reglas incorporadas; `sldb.api.tag_tree`, `tag_folder` y reexporte de `sldb.api.semantic`; CLI `sldb tags namespaces|tree|check`; `sldb.api.replace_text` transaccional con conteo exacto, re-extracción, validación y re-track; CLI `sldb docs replace`; tests, docs y CHANGELOG. Límites: no editar `payload_save_steps.py`; no introducir nombres deskops en `src/sldb/` ni tests; no cambiar salidas existentes; no migrar tags de deskops; no tocar `desk/` salvo lo indicado. No es agregado; es `task.code`.

## AMBIGUEDADES

1. “con los dos Anchor pasa” y “sin Anchor de area:a falla nombrando area:a”: no queda claro si los dos anclas son `area:a` y `area:a.b`, u otras. Obliga a inventar el fixture y si el tag completo requiere ancla.
2. “un archivo no modelado bajo la raíz”: no se define “raíz”. Obliga a inventar la resolución de rutas y el confinamiento.
3. “tag_folder(tag) → ruta a/b para a.b”: no se especifica qué devuelve para tags sin punto, vacíos o con puntos extremos. Obliga a inventar contrato y errores.
4. “orphans: tags usados sin documento ancla, unplaced: documentos ancla sin uso”: no se define la forma de cada elemento. Obliga a inventar el esquema JSON del envelope y de la API.
5. “exige exactamente count apariciones”: no se define conteo solapado, encoding ni normalización. Obliga a inventar semántica de coincidencia.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, `store_declaration.py`, `semantic_tags.py`, módulos `api/rules`, `transaction`, save/extracción, CLI y tests existentes. Cambiaría: campo `tag_namespaces`; nuevo `builtin_tag_rules.py` enganchado en `rules_on_write/check/on_check/explain`; `api/tags/`; `replace_text.py`; reexportes; parsers/comandos CLI; tests, docs y CHANGELOG. Dependencias: GD24 (`sldb.api.transaction`) y GO08 (reglas); rebase sobre `origin/main`; aviso a `w1:p4`. Validaría con `pytest` de los archivos listados, grep de genericidad, `sldb tags tree` y `docs replace --format json` sobre store temporal, `test_clean_code_rules.py`, y coincidencia `files`/diff. Sin ejecutar nada.

## FUTURO

El supervisor decide revisiones en frío, ejecuta la suite completa y valida el resultado integrado. El coordinador poda archivos autorizados no usados, avisa a `w1:p4` y dispone hallazgos. deskops recibe la nota de cierre, migra sus tags y satisface `G_GD27`. El dueño decide si q3 debe convertirse en RuleDoc de usuario.
