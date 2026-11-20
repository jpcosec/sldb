PASA

# Resultado de testing

Task: `task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen`
Commit del ejecutor: `3f547569b90fc28aa3d5ef5be5ea20ca2b9d61ea`
Base contra la que se probó la regresión: `6df00576242d74b33738c18a4e19aead3b8841fa`

## Veredicto

PASA. Los tests del commit pasan, las pruebas de regresión fallan en el commit padre y pasan con el arreglo, `bash tools/check.sh --fast` termina en 0, y `deskops next` de la tarea de sldb move en el repo real ya no muestra `Blocked by` (la tarea aparece en `ritual-execution`).

## Archivos del commit revisados

- `src/sldb/store/edge_index/cache_keys.py`: `roster_state()` incorpora el `roster_hash` de cada modelo.
- `src/sldb/store/edge_index/composed_disk.py`: la clave de la caché compuesta incluye `roster_state(p)` por store.
- `src/sldb/store/layout.py`: `drop_disk_caches()` borra `composed/*.json` y `document_rows/*.json`.
- `src/sldb/api/stores/build_store.py`: `stores build` invoca `drop_disk_caches()`.
- `tests/api/test_select_documents_disk.py`: dos tests nuevos (reescritura in-place con reloj detenido; build sin caché vieja).
- `CHANGELOG.md`: entrada correspondiente.

No existían `tests/test_build_store.py`, `tests/test_cache_keys.py`, `tests/test_composed_disk.py` ni `tests/test_layout.py`; se corrieron los tests existentes más cercanos a cada módulo tocado y a la superficie afectada.

## Tests ejecutados (de a uno)

Comando base: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider <archivo>` con el Python del venv (`/tmp/ws-venv`, enlazado al `.venv` del repo porque `/tmp/ws-venv` no existía al inicio).

| Archivo | Resultado |
|---|---|
| `tests/api/test_select_documents_disk.py` | 8 passed |
| `tests/api/test_select_documents.py` | 19 passed |
| `tests/api/test_doc_anchors.py` | 24 passed |
| `tests/api/test_views.py` | 17 passed |
| `tests/api/test_composition_edges.py` | 7 passed |
| `tests/api/test_composition_ref_root.py` | 3 passed |
| `tests/store/test_stores_build.py` | 35 passed |
| `tests/api/test_api_stores.py` | 14 passed |
| `tests/store/test_cache_identity.py` | 3 passed |
| `tests/store/test_live_stale_security.py` | 8 passed |
| `tests/store/test_shard_cache_copies.py` | 4 passed |
| `tests/store/test_runtime_cache_outside_store.py` | 3 passed |
| `tests/api/test_rules.py` | 13 passed |
| `tests/api/test_rules_end_to_end.py` | 1 passed |

No se corrió la suite completa, según la indicación del rol.

## Prueba de que los tests nuevos cubren la regresión

En un worktree temporal en el commit padre (`6df0057`), copiando el test nuevo del commit:

- `test_a_rewrite_in_place_inside_one_clock_tick_is_seen_by_the_next_process`: FALLA en el padre (`[] != ['TaskDoc:b']`).
- `test_a_store_build_leaves_no_disk_cache_of_the_old_state`: FALLA en el padre (queda `composed/old.json`).

En el commit del ejecutor ambos pasan.

## Gates rápidos

`PATH=/tmp/ws-venv/bin:$PATH bash tools/check.sh --fast` → rc 0, `TODAS LAS PUERTAS PASAN`
(núcleo aislado, capas, identidad, ejes y superficie; se omiten las lentas, como corresponde a `--fast`).

## Verificación del Done When en el repo real

Ejecutado (solo lectura, `next` no muta):

`PYTHONPATH=src:/mnt/ssd/proyectos/SLDB_1/deskops /tmp/ws-venv/bin/python -m deskops.cli.main next task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer --root .`

Resultado: rc 0, sin `Blocked by`; la tarea de sldb move aparece con `Status: draft` y `Current node: ritual-execution`. Esto confirma que la caché vieja del repo se invalida sin borrar `.sldb_cache` a mano.

## Observaciones

- `/tmp/ws-venv` no existía; se creó un enlace simbólico al `.venv` del repo para ejecutar con el mismo Python y dependencias. No es un cambio del repo.
- El worktree temporal usado para la prueba de regresión fue eliminado al terminar.
