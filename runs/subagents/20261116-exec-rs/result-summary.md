# Ejecutor deskops-e-4301e4e74c7c — result summary

Task: `task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared`. Pills: ninguno.

## Cambios
- `src/sldb/api/stores/read_store.py`, `read_store`: después de resolver el store, si el directorio `.sldb` resuelto no existe (`not Path(store_path).is_dir()`) lanza `SLDBStoreError("store not found: <ruta .sldb resuelta>")` (constante nueva `NOT_FOUND`). El mensaje `store not prepared: run \`sldb stores update\` (<ruta>)` no cambia. Docstring (Raises) actualizado. `store_is_prepared` **no** cambia (decisión 1 del coordinador).
- `tests/api/test_api_stores.py`: `test_read_store_says_not_found_when_the_store_directory_does_not_exist` (mensaje empieza por `store not found: `, contiene la ruta resuelta, no dice "not prepared", no crea el directorio) y `test_read_store_says_not_prepared_when_the_store_exists_without_its_index` (`.sldb` vacío → `store not prepared: run \`sldb stores update\` (`).
- `CHANGELOG.md`: entrada en 0.1.13.

## Done When
- Validation pasa con los tests nuevos: sí (ver abajo y `validation.log`).
- CHANGELOG: sí. Commit y aviso a graph_ui: **no**, por decisión 4 del coordinador (no commit, no avisos); quedan para el coordinador/closeout.

## Comandos (todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
- `pytest -q tests/api/test_api_stores.py` → rc=0 (14 passed)
- `pytest -q tests/test_clean_code_rules.py` → rc=0 (1206 passed)
- `bash tools/check.sh --fast` → rc=0 (TODAS LAS PUERTAS PASAN)
Suite completa y `sldb stores build --check`: no figuran en Validation; no corridos.

## Archivos tocados
- src/sldb/api/stores/read_store.py
- tests/api/test_api_stores.py
- CHANGELOG.md
(+ esta entrega en runs/subagents/20261116-exec-rs/)

## Otros puntos con 'not prepared' (decisión 3, sin cambiar)
`grep -rn "not prepared\|NOT_PREPARED\|store_is_prepared" src`: fuera de `read_store.py` solo aparece el re-export en `src/sldb/api/__init__.py:124` y `:170` (`read_store`, `store_is_prepared`). Ningún otro punto de la API lanza 'not prepared'. Usuarios de `store_is_prepared` en el repo: solo los tests de `tests/api/test_api_stores.py` (los usuarios externos, p. ej. graph_ui, no están en este repo).

## Desvíos / dudas
- El mensaje usa `store_path` tal como lo devuelve la resolución: `_resolve_store_arg` ya devuelve `Path(...).resolve()`; `_find_default_store` devuelve el store encontrado o el global resuelto.
- Un `store` que es un alias no registrado cae en el path candidato resuelto y, si no existe, ahora da 'store not found: <ruta>' (antes 'not prepared').
- graph_ui solo traduce a 503 la substring 'store not prepared'; el nuevo mensaje le llegará como error genérico (lo previsto por la nota del inbox).
