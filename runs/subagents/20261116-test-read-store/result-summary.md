# Tester deskops-t-aaa566ba1025 — read_store / store_is_prepared / extract_payload

Veredicto: **PASA** (todo lo verificable por el tester; commit y aviso a graph_ui quedan para el closeout del coordinador).

Entorno: todos los comandos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev` (uv funcionó; no hizo falta el fallback). Salida completa en `validation.log`.

## Validation

| Comando | Resultado |
|---|---|
| `pytest -q tests/api/test_api_stores.py` | PASA — 12 passed, rc 0 |
| `pytest -q tests/store/test_legacy_layout_migration.py` | PASA — 3 passed, rc 0 |
| `bash tools/check.sh --fast` | PASA — "TODAS LAS PUERTAS PASAN", rc 0 |
| (4.º comando que el contrato menciona pero no lista) | n/a — Validation lista tres; corrí además el `python -c` de Done When |

## Done When, punto por punto

- Comandos de Validation pasan: **PASA** (tabla de arriba).
- `python -c "from sldb.api import read_store, store_is_prepared, extract_payload"`: **PASA** — rc 0; además los tres nombres están en `sldb.api.__all__` (imprime `True`).
- Test de cero escrituras (`test_read_store_writes_nothing_on_a_prepared_store`) y de store no preparado (`test_read_store_refuses_an_unprepared_store_and_leaves_it_unmigrated`): **PASA** — incluidos en los 12; leídos: el primero compara el conjunto `(ruta, mtime_ns, tamaño)` bajo el proyecto, como pide Precisiones; el segundo usa un store de layout viejo armado copiando la fixture de `test_legacy_layout_migration.py`, comprueba `SLDBStoreError` con el texto exigido, snapshot igual y `store_index.yaml` aún en la raíz.
- CHANGELOG: **PASA** — una línea en español bajo `## 0.1.13 — not released yet`, primera de la sección, estilo de las vecinas.
- Doc: **PASA** — sección corta en `docs/architecture/store-declaration.md` sobre `open_store` vs `read_store` (el archivo que fija Precisiones).
- Commit: **no aplica al tester** — lo hace el coordinador con `deskops closeout commit`; nada commiteado todavía.
- Mensaje a graph_ui: **pendiente del closeout** — no enviado; el ejecutor dejó el texto propuesto en su informe.

## Revisión del código contra Scope/Precisiones

- `read_store`: resuelve igual que `open_store` (`_resolve_store_arg(str(store))` si truthy, si no `_find_default_store("readonly")`), `project_root`, comprueba `store_is_prepared` o lanza, y luego `add_owner_import_roots` → `new_operation` → `new_documents_hash_operation` → `StoreLocation`. No importa ni llama `migrate_store_layout`. Orden conforme.
- `store_is_prepared`: False si no hay `store_exists` o falta `store_index_path`; si no, `_already_canonical(load_store_index(...), store_path, project_root(...))`, importado de `sldb.store.migration` (no movido). `migration.py` y `open_store.py` sin cambios (`git diff --quiet`).
- `extract_payload(model_type, markdown)` = `extract_model_data(model_type, markdown)`.
- Desvío menor (ya anotado por el ejecutor): el mensaje es `store not prepared: run \`sldb stores update\` (<ruta>)` — contiene el texto del Goal íntegro y añade la ruta. Lo considero aceptable.
- Nota: `sldb.runtime.validation` ya tiene otra `extract_payload(template, markdown)`; el nombre se repite en dos módulos sin colisionar.

## Casos extra del tester (no cubiertos por el ejecutor)

Script `/dev/shm/tester-read-store/test_edges.py` (fuera del repo), 5 passed, rc 0:

1. `test_no_write_syscalls_audit_hook`: con `sys.addaudithook`, durante `read_store` sobre un store preparado no hay `open` en modo escritura/creación, ni `rename/replace/mkdir/remove/rmdir/truncate`, bajo el proyecto. Más estricto que la comparación de mtimes.
2. `test_canonical_location_but_unsharded_semantic_index_is_refused`: un store **en ubicación canónica** (`core/store_index.yaml`) pero con el índice semántico viejo sin shardear (`semantic_index_path`) → `store_is_prepared` False, `SLDBStoreError` con el texto exigido, cero escrituras y el archivo viejo sigue ahí (es decir, no solo detecta el layout de raíz).
3. `test_missing_store_path_raises_and_creates_nothing`: ruta inexistente → `SLDBStoreError` y no se crea ningún directorio.
4. `test_sees_removal_by_another_process_path`: una **baja** (`untrack_document`, vía `open_store`) entre dos `read_store` se ve en el segundo (el ejecutor solo probó una alta).
5. `test_discovery_from_cwd`: `read_store()` y `read_store("")` con cwd en el proyecto resuelven el store del proyecto.

(La primera corrida del script falló por un error mío — faltaba `PYTHONPATH=.` y una firma mal escrita de `untrack_document` —; queda registrada en `validation.log` y la corrida corregida pasa.)

## Alcance de los cambios

Del ejecutor: `src/sldb/api/stores/read_store.py` (nuevo), `src/sldb/api/documents/extract_payload.py` (nuevo), `src/sldb/api/__init__.py`, `tests/api/test_api_stores.py`, `CHANGELOG.md`, `docs/architecture/store-declaration.md` (autorizado en Scope/Precisiones aunque no está en `files:`). Nada fuera del contrato.

Otros cambios en el árbol: los ajenos que lista el brief (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`) y además `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models/RunDoc.yaml` y dos `RunDoc` nuevos: son el registro de corridas (includes de `run.md` de este ejecutor y este tester, store_hash) que hace el coordinador; ya estaban al empezar esta sesión y no son del ejecutor. No los toqué.
