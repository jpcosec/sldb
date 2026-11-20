PASA

# result-summary: arreglo de 3f547569 (caché vieja de ReviewDoc)

Commit del ejecutor: `3c04f6f9dac7d159dff0f61d8349dd31857cbd29` (`Task-Id: task-arreglo-de-3f547569-...`).

## Qué se verificó

- `layout.py` ya no contiene `drop_disk_caches`: el commit lo mueve a `src/sldb/store/disk_caches.py` y `build_store.py` importa desde ahí. `tests/test_clean_code_rules.py` pasa completo (1226 tests), sin tocar el límite de 80 líneas.
- El test de reescritura en el mismo tick construye el subproceso con el `sldb` bajo prueba (`Path(sldb.__file__).parent.parent` insertado al frente de `sys.path`), no con un editable install de otro checkout. El test sigue comprobando el comportamiento real: crea el Review, lee (puebla caché), reescribe en sitio sin mover el reloj, restaura los stamps y exige que el siguiente proceso vea `TaskDoc:b`.
- Las cachés de filas de documentos y compuesta incluyen el `roster_hash` de cada modelo (`document_rows_disk.py`, `composed_disk.py`, `cache_keys.py`), por lo que la reescritura in place se detecta.

## Comandos y resultados

Entorno: `TMPDIR=/tmp PATH=/tmp/ws-venv/bin:$PATH` (venv del repo; se instaló `pytest-xdist` porque no estaba). Todos desde la raíz de sldb.

| comando | resultado |
|---|---|
| `python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py` | 8 passed |
| `python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py` | 1226 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_api_stores.py` | 14 passed |
| `python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py` | 35 passed |
| `python -m pytest -q -p no:cacheprovider tests/store/test_migrate_layout.py` | 8 passed |
| `python -m pytest -q -p no:cacheprovider tests/store/test_legacy_layout_migration.py` | 3 passed |
| test de reescritura suelto, 20 veces seguidas | 20/20 passed |
| `python -m pytest -q -p no:cacheprovider -n 4 tests/api` | 657 passed, 8 skipped |
| `bash tools/check.sh --fast` | rc 0, todas las puertas pasan |

## Notas

- La suite completa no se corrió acá (la corre integrate en el host), según el encargo.
- `pytest-xdist` no estaba en el venv; se instaló con `uv pip install --python .venv/bin/python pytest-xdist` para poder correr `-n 4`. No se tocó código ni tests.
- El árbol de `src/`, `tests/`, `contracts/` y `CHANGELOG.md` está en el commit del ejecutor, sin cambios locales.
