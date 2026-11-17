# Result: executor deskops-e-13131c57ccbe

Tarea: task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse.
Leí también review bundle-2 (aceptada): inventario = toda función sin `_` inicial de src/sldb/api con parámetro `actor`; `actor=None` conserva lo que el código hace hoy. Pills: ninguno.

## Cambios
- `src/sldb/api/anchors/anchor_docs.py`
  - `write_anchor`: nuevo último parámetro `actor: str | None = None`; lo pasa a `create_document` (anchor nuevo) y a `save_document_payload` (re-registro). Docstring lo dice.
  - `record_reconnection`: nuevo parámetro `actor: str | None = None` (último); antes llamaba `save_document_payload(..., actor=None)` fijo. El único caller (`check_anchors`) no lo pasa: comportamiento igual.
  - `actor=None` → `current_actor(None)` en `stamped`, exactamente como hoy (proceso / `SLDB_ACTOR` / `agent`).
- Docstrings (autorizado por Scope: "se documenta en su docstring"):
  - `src/sldb/api/semantic/dag_writes.py`: `add_semantic_parent`, `remove_semantic_parent`, `add_semantic_equivalence` dicen que `actor` no se registra (el DAG no es un documento, no hay bloque que firmar). Antes solo lo decía el helper privado `_refreshing`.
  - `src/sldb/api/documents/delete_document.py`: el arg `actor` decía "stamped into the document's provenance block", falso (el archivo se borra); ahora dice que no se registra.
- `tests/api/test_provenance.py`: fixture `anchored` (skip sin tree-sitter) y 3 tests: `test_write_anchor_signs_with_its_actor_when_it_creates_and_when_it_re_records` (crear → `agent:anchor`/create_document; re-registrar → `human:jp`/save_document_payload; `actor=None` → `agent`), `test_a_reconnection_is_signed_by_the_actor_it_is_given`, `test_no_public_write_function_drops_its_actor_without_saying_so` (recorre con `ast` src/sldb/api y falla si una función pública con `actor` no lo lee ni dice "not recorded"/"no longer recorded" en su docstring).
- `CHANGELOG.md`: entrada en 0.1.13.

## Inventario (funciones públicas de src/sldb/api con `actor`)
Pasan actor hasta el sello `sldb.by`:
- documents: `create_document`, `save_document_payload`, `write_rendered_document`, `stamped`, `stamped_file`
- anchors: `write_anchor` (arreglada), `record_reconnection` (arreglada)
- model_drafts: `promote_model_draft` → `apply_backfill` → `stamped_file`
- notations: `save_projection_view`, `sync_spec`, `sync_palette`, `sync_notation`, `SpecSync.__init__`, `StoreWriter.__init__` (→ create/save/delete_document y add_model)
- `create_model` → `add_model` (ver abajo); `set_actor` (fija el actor del proceso)

Excepciones (no hay documento que firmar; documentado en docstring):
- `track_document_file` (no reescribe el archivo, por diseño: test existente "track does not rewrite the file"), `untrack_document`, `add_model`, `inherit_model`, `reindex_model`, `remove_model` — ya documentadas ("no longer recorded", journal retirado 2026-11-04).
- `delete_document` (borra el archivo; lo pasa a `untrack_document`) — docstring corregido.
- `add_semantic_parent`, `remove_semantic_parent`, `add_semantic_equivalence` — docstring añadido.

## Done When
- Validation pasa con los tests nuevos: sí (ver abajo).
- Ninguna función pública de escritura descarta actor: las que firman lo pasan; las que no pueden lo dicen en su docstring; lo fija el test de inventario.
- CHANGELOG: sí. Commit: NO hecho (prohibido por brief y por el coordinador); queda para el closeout.

## Comandos (salida completa en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py` → rc 0 (10 passed)
- `... pytest -q tests/api/test_anchors.py` → rc 0 (23 passed)
- `... pytest -q tests/api/test_api_documents.py` → rc 0 (17 passed)
- `... pytest -q tests/test_clean_code_rules.py` → rc 0 (1206 passed)
- `... bash tools/check.sh --fast` → rc 0
Suite completa y `sldb stores build --check`: no figuran en Validation; delegados al integrador.

## Archivos tocados
- src/sldb/api/anchors/anchor_docs.py
- src/sldb/api/semantic/dag_writes.py (solo docstrings)
- src/sldb/api/documents/delete_document.py (solo docstring)
- tests/api/test_provenance.py
- CHANGELOG.md

## Desvíos / dudas
- dag_writes.py y delete_document.py están fuera de la lista `files` del frontmatter; los toqué solo en docstrings, al amparo del Scope ("si alguna no puede respetarlo, se documenta en su docstring").
- `record_reconnection` no tenía `actor`; la incluí porque el Rationale la cita (anchor_docs.py:47 con `actor=None`) y bundle-2 deja la decisión al ejecutor. `check_anchors` no recibe actor y no se cambió (fuera de alcance): una reconexión desde `check_anchors` sigue firmada por el actor del proceso, como hoy.
- No se tocaron los cambios ajenos del árbol.
