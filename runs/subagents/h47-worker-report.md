# h47-worker: informe (H4-H7)

## Estado actual (commiteado antes del cambio)

- H4: `check_on_write` (`api/rules/rules_on_write.py`) solo se llama desde `save_document_payload`
  (`payload_save_steps.check_rules_on_write`). `create_document` y `track_document_file` no lo llaman;
  por eso un documento con tags sin ancla entra y solo `on_check` lo ve (rules.md H-GO08-6).
- H5: `declare_store._kept` conserva solo `generate` y `derived` de la declaración vigente. Las demás
  claves autoradas de `StoreDeclaration` que un índice no puede decir (`tag_namespaces`, `tag_models`,
  `policy`, `graph_backend`, `folders`, `seeds`, `project_graph`) se pierden con `stores declare --write`.
- H6: el hallazgo de la familia lleva su evaluación solo como texto (`cláusula (seen: {json})`);
  `tags check --format json` devuelve únicamente `findings`.
- H7: tags.md y rules.md no dicen que la familia solo ve documentos indexados.

## Aceptación línea por línea

| Aceptación | Evidencia |
|---|---|
| Estado actual primero, commiteado antes del cambio | commit `a5288b22` (este informe, sección anterior) precede a q1-q5 |
| q1 (H5) declare --write conserva las claves autoradas | `tests/api/test_declare_store_authored.py`: una declaración con `tag_namespaces`, `tag_models`, `policy`, `graph_backend`, `folders`, `seeds`, `project_graph` y `derived` queda igual tras `declare_store` |
| q2 (H4) create/track evalúan on_write | `tests/api/test_on_write_entering.py` (7 casos, ver tabla); código en `api/documents/on_write_gate.py`; contrato en rules.md §9.1 y H-GO08-6 |
| q3 (H6) evaluación estructurada | `sldb.api.tag_evaluations(store)` y clave `evaluations` de `tags check --format json`; test `test_tags_check_gives_the_evaluation_as_data_beside_the_findings` |
| q4 (H7) guía | tags.md §«Which documents the family sees (H7)» |
| q5 tests y docs | tests citados, CHANGELOG, rules.md, tags.md |
| test_clean_code_rules | verde en la suite completa (tras separar `builtin_tag_findings.py` y `_admit` en create_document; ningún límite subido) |
| `tools/check.sh --fast` | PASS en las 5 puertas (núcleo, capas, identidad, ejes 31/750, superficie); no hizo falta tocar `contracts/layers.toml` |
| Suite completa | 187 archivos `tests/**/test_*.py`, cada uno en su pytest desde copia en /dev/shm con wait-pytest: **2409 passed, 0 failed**; 5 archivos 100 % skipped (test_anchors 7, test_machine_editor_schema 7, selfdoc/test_fingerprints 4, test_treesitter_agreement 2, test_treesitter_symbols 4: dependencia opcional ausente, no es del cambio) |

## Casos probados

| Caso | Resultado |
|---|---|
| create viola on_write | SLDBRuleViolationError, ni archivo ni nodo |
| create cumple | escrito y trackeado |
| track de archivo a mano que viola | rechazado, el archivo queda, no se trackea |
| track que cumple | trackeado |
| apply_batch con create válido + create inválido | rechazo, árbol sin ninguno de los dos |
| transaction.create válido + inválido | rechazo, árbol restaurado |
| store sin reglas on_write | crea como antes |
| declare --write con todas las claves autoradas | idéntico |
| tags check JSON | `evaluations` con held/no held, `missing`, sin parsear texto |
| tag_evaluations sin namespaces | `[]` |

`stores build` no evalúa on_write: no cambié `apply_includes`; no añadí test negativo propio (queda cubierto por no haberlo tocado y por la suite de `tests/store/test_stores_build.py` en verde); la decisión está escrita en rules.md §9.1 y tags.md.

## Decisiones y desvíos

- H5: además de `tag_namespaces` y `tag_models` declare --write perdía `policy`, `graph_backend`, `folders`, `seeds` y `project_graph`; se suman (en alcance, regla 3).
- H6: nombres elegidos: `tag_evaluations` (api, `sldb.api.tags`) y `tag_report` (api.tags, devuelve findings y evaluations en una pasada). Entrada: `{document, namespace, rule, holds, clause, tags, missing}`. **Desvío:** `rules check --format json` NO lleva `evaluations` (la disposición de pi lo limita a `tags check`; `rules explain` ya devolvía node/holds/clause/seen).
- `track_document_file(force=True)` de un archivo que el modelo no extrae no se evalúa (no hay payload); sin `force` el round-trip falla antes.
- Tests existentes ajustados porque dependían del comportamiento anterior: `test_tags.py` y `test_tags_scope.py` creaban huérfanos con `create_document` (ahora lo rechaza; se crean antes de declarar los namespaces, helper `orphan`); `test_referrers.py` daba por buena la pérdida de `project_graph` de declare --write.
- Código movido por los límites de código limpio: `store_findings`, `family_*`, `findings_of`, `_finding` a `api/rules/builtin_tag_findings.py` (sin cambio de comportamiento).
- Entorno: no hay `python` en PATH; usé `~/proyectos/SLDB_1/.venv/bin/python` con `PYTHONPATH=<copia en /dev/shm>/src` (sldb de ese venv es sldb-runtime, no se importó). La copia en /dev/shm fue un rsync del worktree (con .sldb y desk, que los tests leen), no un `git worktree add`.

## Hipótesis para el resto del ecosistema

- deskops: el puente que repite la validación de tags puede borrarse (otra tarea); puede leer `tag_evaluations` en vez de parsear el texto del hallazgo.
- deskops: cualquier flujo que cree documentos con tags sin ancla vía `create_document` ahora recibe SLDBRuleViolationError; si necesitaba crear huérfanos, debe declarar los namespaces después.
- sldb: `rules check` podría ganar `evaluations` si deskops lo pide.

## Tests existentes modificados: qué afirmación cambió y por qué

Ninguna aserción sobre hallazgos, mensajes de error o estado del índice se relajó; cambia cómo se llega al estado de prueba o qué forma tiene la salida JSON.

### tests/api/test_tags.py

- Helper nuevo `World.orphan(name, tags)`: guarda la declaración, la deja sin namespaces, crea la nota y restaura la declaración. **Por qué:** estos tests necesitan un documento que ya viola la familia para probar `tags check`, `rules check`, `rules explain` y `tag_tree` sobre huérfanos. Antes lo conseguían con `create_document` porque no evaluaba `on_write`; con H4 ese alta se rechaza con `SLDBRuleViolationError` (rules.md §9.1), así que el huérfano solo puede existir si entró antes de declararse el namespace, que es el caso real que `tags check` y `on_check` cubren.
- `placed.note("n2", ["area:c"])` → `placed.orphan(...)` en tres tests: `test_tags_check_finds_a_document_created_without_its_anchor`, `test_rules_explain_answers_a_builtin_rule_with_its_eval_finding` y `test_tag_tree_lists_the_anchors_the_orphan_and_the_unplaced` (el que ejerce `tag_tree` con el huérfano `area:c`). Las aserciones de esos tests no cambian. Solo cambió el docstring del primero, que decía «`create_document` runs no `on_write` rule (q18, a GO08 gap)», ahora falso.
- `test_tags_check_finds_...`: `envelope["data"] == {"findings": [found.as_dict()]}` → `envelope["data"]["findings"] == [found.as_dict()]`. **Por qué:** `tags check --format json` gana la clave `evaluations` (H6, aditiva), así que la igualdad exacta del dict ya no vale. La lista de hallazgos se sigue comparando entera; la clave nueva se afirma en el test nuevo. `rules check` conserva la comparación exacta `{"findings": [...]}`, porque no cambió.
- `test_tags_check_passes_a_placed_store`: `envelope["data"] == {"findings": []}` → `envelope["data"]["findings"] == []`, mismo motivo.
- Tests nuevos (H6): `test_tags_check_gives_the_evaluation_as_data_beside_the_findings` y `test_tag_evaluations_are_empty_without_namespaces`.

### tests/api/test_tags_scope.py

Tres tests: `test_tag_models_checks_only_their_documents_and_descendants`, `test_tag_tree_with_tag_models_uses_only_documents_in_scope_and_every_anchor` y `test_without_tag_models_the_declaration_dumps_as_before_and_every_document_is_checked`. **Único cambio: la línea `desk.declare(...)` pasa de antes a después de los `desk.create(...)`.** Las aserciones no cambian. **Por qué:** los tres crean documentos que violan la familia (`workspace:x` sin namespace declarado, `kind:x`, `pill-type:y`, `domain:d` sin ancla) para comprobar que `tag_models` los acota. Declarando primero, `create_document` los rechaza por H4 (el fallo que vimos fue `rules/builtin:tag_namespace:workspace: namespace declared`). Declarando después queda el mismo estado que antes (documentos indexados que violan la familia) y las comprobaciones de alcance de `tag_models` siguen ejerciéndose igual. El cuarto test del archivo (`explain` fuera de alcance) pasaba sin cambios.

### tests/api/test_referrers.py

`test_a_store_without_a_project_graph_has_only_the_fields`: antes `save_declaration(store, declare_store(...))`; ahora `declared = declare_store(...)` y se guarda `declared.model_copy(update={"project_graph": None})`. La aserción (`referrers` solo devuelve las menciones de campos, `EXPECTED[:3]`) no cambia. **Por qué:** el test usaba `declare_store` como forma de obtener un store sin `project_graph`, o sea que dependía de que `declare --write` perdiera esa clave, que es justo el bug que corrige H5. Ahora la declaración conserva el `project_graph` del fixture, y el test lo quita explícitamente para seguir probando «store sin project graph».

### Qué mirar al integrar

El único cambio de contrato visible para un consumidor externo es el de `tags check --format json` (clave nueva `evaluations`, aditiva) y el rechazo del alta. Si deskops compara `data == {"findings": ...}` de `tags check` con igualdad exacta, tendrá que ajustarlo igual.
