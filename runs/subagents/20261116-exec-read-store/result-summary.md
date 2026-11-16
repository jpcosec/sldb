# Resultado — executor deskops-e-ec3e43f4e6ca

Task: `task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n`. Pills atados: ninguno (sin choques que anotar).

## Cambios

- `src/sldb/api/stores/read_store.py` (nuevo):
  - `store_is_prepared(store) -> bool`: False si no hay store (`store_exists`) o falta `core/store_index.yaml` (`store_index_path`); si no, `_already_canonical(load_store_index(store_path), store_path, project_root(store_path))`. `_already_canonical` se importa de `sldb.store.migration` (no se mueve ni cambia).
  - `read_store(store=None) -> StoreLocation`: resuelve igual que `open_store` (`_resolve_store_arg(str(store))` si es truthy, si no `_find_default_store("readonly")`), `project_root`, comprueba `store_is_prepared` o lanza `SLDBStoreError("store not prepared: run `sldb stores update` (<store_path>)")`, luego `add_owner_import_roots`, `new_operation`, `new_documents_hash_operation` y devuelve `StoreLocation`. No llama `migrate_store_layout`.
- `src/sldb/api/documents/extract_payload.py` (nuevo): `extract_payload(model_type: type, markdown: str) -> dict[str, Any]` = `extract_model_data(model_type, markdown)`.
- `src/sldb/api/__init__.py`: imports y `__all__` de `read_store`, `store_is_prepared`, `extract_payload`.
- `tests/api/test_api_stores.py`: helpers `_snapshot` (conjunto `(ruta, mtime_ns, tamaño)`) y `_legacy_store` (copia de lo que hace `_legacy_store`/`_write_model_files` de `tests/store/test_legacy_layout_migration.py`, sobre `_store` de `tests/store/test_documents_shards.py`); tests nuevos:
  - `test_read_store_writes_nothing_on_a_prepared_store`
  - `test_read_store_refuses_an_unprepared_store_and_leaves_it_unmigrated` (también compara snapshot y que el `store_index.yaml` siga en la raíz)
  - `test_store_is_prepared_is_false_without_a_store`
  - `test_read_store_sees_a_document_added_by_another_open_store` (el alta va por `track_document_file`, que abre con `open_store`)
  - `test_extract_payload_matches_extract_model_data`
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet`.
- `docs/architecture/store-declaration.md`: sección corta "Reading a store: `open_store` and `read_store`" (autorizado en Precisiones).
- `src/sldb/store/migration.py`: sin cambios (el contrato permite reexportar; se importa directo).

## Done When

- Los comandos de Validation pasan (ver abajo; el contrato dice "cuatro", Validation lista tres; corrí los tres más el `python -c`).
- `python -c "from sldb.api import read_store, store_is_prepared, extract_payload"` → rc 0.
- Test de cero escrituras y de store no preparado: pasan.
- CHANGELOG y doc: hechos. Commit: lo hace el coordinador (`deskops closeout commit`); no hice commit.
- Mensaje a graph_ui: no enviado por mí (el brief prohíbe tocar desk/ y el contrato lo pone "al cerrar"). Texto propuesto:
  Aviso a graph_ui: sldb.api exporta `read_store(store) -> StoreLocation` (operación nueva de solo lectura, sin migrar; `SLDBStoreError` "store not prepared: run `sldb stores update`" si el layout no es canónico), `store_is_prepared(store) -> bool` y `extract_payload(model_type, markdown) -> dict`; reemplazan `open_store(mode="readonly")`, `new_operation` de `sldb.store.runtime_cache_signature`/`documents_hash` y `sldb.runtime.validation.extract_model_data`. Commit: <el del closeout>.

## Comandos (salida completa en validation.log)

Todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`:
- `pytest -q tests/api/test_api_stores.py` → rc 0 (12 passed)
- `pytest -q tests/store/test_legacy_layout_migration.py` → rc 0 (3 passed)
- `bash tools/check.sh --fast` → rc 0 (TODAS LAS PUERTAS PASAN)
- `python -c "from sldb.api import read_store, store_is_prepared, extract_payload; print('ok')"` → rc 0

## Archivos tocados

- src/sldb/api/stores/read_store.py (nuevo)
- src/sldb/api/documents/extract_payload.py (nuevo)
- src/sldb/api/__init__.py
- tests/api/test_api_stores.py
- CHANGELOG.md
- docs/architecture/store-declaration.md
- runs/subagents/20261116-exec-read-store/{validation.log,result-summary.md}

## Desvíos / dudas

- El mensaje de error añade la ruta del store entre paréntesis tras el texto exigido (el test usa `match`, el texto del Goal está íntegro).
- `sldb.runtime.validation` ya tiene una función `extract_payload(template, markdown)` distinta; la nueva de `sldb.api` tiene la firma del contrato `(model_type, markdown)`. No colisionan, pero el nombre se repite.
- "Cuatro comandos de Validation" vs. tres listados: corrí los tres y el import.
- Cambios ajenos (apply_batch.py, lock.py, uv.lock, .sldb/, desk/runtimes/…) no tocados.
