FALLA

# Testing — persistencia del conjunto de documentos sucios en `.sldb_cache`

Task: `task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent`
Commit del ejecutor: `6772820a48ee1f43a57a32bc9a45c3509400af38` — `Persist the dirty document set in .sldb_cache so incremental mode works across processes`
Archivos del commit: `src/sldb/store/documents_dirty.py`, `src/sldb/store/documents_dirty_persist.py`, `tests/store/test_merkle_operation_cache.py`, `contracts/layers.toml`, `CHANGELOG.md`.

## Veredicto

**FALLA formal por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**:
la puerta `identidad` rechaza el directorio versionado `workbench_demo` («directorio versionado sin
clasificar en la raíz»). La regla del rol es explícita: rc distinto de 0 en `check.sh --fast` ⇒ FALLA.

La roja es **preexistente y ajena a este commit**: `workbench_demo` entró versionado en `562847e2`,
ya es ancestro del commit del ejecutor, y este no toca `workbench_demo` ni `contracts/identity.toml`.
El resto de las puertas rápidas (`núcleo aislado`, `capas`, `ejes`, `superficie`) pasa.

**No encontré un defecto funcional en el cambio.** Los tests de la tarea, los módulos tocados y
`tests/test_clean_code_rules.py` pasan. Si el coordinador acepta formalmente la excepción conocida
de `identidad`/`workbench_demo`, el trabajo está listo para cerrar.

## Validación ejecutada

`/tmp/ws-venv` no existe en este host y no hay `uv` disponible. Usé el venv del repo,
`/workspace/sldb/.venv/bin/python` (Python 3.13.18), con `TMPDIR=/tmp`, un archivo por corrida y sin
`-p no:cacheprovider`:

| Comando | rc | Resultado |
|---|---|---|
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/store/test_merkle_operation_cache.py` | 0 | **9 passed** (6 previos + 3 nuevos) |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/store/test_runtime_wiped.py` | 0 | **1 passed** |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/store/test_edges_follow_the_contract.py` | 0 | **1 passed** |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/test_clean_code_rules.py` | 0 | **1237 passed** |
| `PATH=/workspace/sldb/.venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast` | **1** | Falla **solo** `identidad` por `workbench_demo`; pasan `núcleo aislado`, `capas`, `ejes`, `superficie` |

Regresiones relacionadas adicionales (no la suite completa):

| Comando | rc | Resultado |
|---|---|---|
| `tests/store/test_merkle_cost.py tests/store/test_shard_cache_copies.py tests/store/test_runtime_cache_outside_store.py` | 0 | **9 passed** |
| `tests/store/test_documents_shards.py tests/store/test_models_io.py` | 0 | **14 passed** |

No existen `tests/test_documents_dirty.py` ni `tests/test_documents_dirty_persist.py`; el test del
módulo tocado es `tests/store/test_merkle_operation_cache.py`, ya corrido.

## Comportamiento comprobado

- El archivo es `<store>/../.sldb_cache/documents_dirty.json` (`layout.cache_dir`), fuera de Git por
  `.gitignore` (`.sldb_cache/`).
- JSON `{"signature": <cadena>, "entries": [[modelo, namespace, [nombres...]], ...]}`; la firma es
  `json.dumps(list(runtime_cache_signature.signature(s_path)), default=str)` y se compara por
  igualdad de cadena.
- Escritura atómica: temporal con el PID + `os.replace`, dentro de `store_lock(..., wait=True)`.
- Carga perezosa por `str(s_path)`: la primera `names()` lee el archivo una vez; `_LOADED` evita
  releerlo. `mark`, `clear` e `invalidate` reescriben el archivo del store.
- Un proceso nuevo ve el dirty set dejado por el anterior (`['note-0']`) y `None` para un modelo sin
  baseline. Un archivo corrupto (JSON inválido, faltan claves o `entries` con otra forma) se borra y
  `names()` devuelve `None`, sin log ni error. Un cambio en la firma del store también invalida y
  borra el archivo.
- `documents_dirty.py` queda en 56 líneas y la lógica nueva está en `documents_dirty_persist.py`
  (86 líneas de archivo); `tests/test_clean_code_rules.py` no reporta violaciones.
- `contracts/layers.toml` incorpora el módulo nuevo al eje `op_documentos`; la puerta `capas` pasa.
- CHANGELOG: entrada presente y coherente con el comportamiento implementado.

## Observaciones no bloqueantes

- La roja de `identidad` por `workbench_demo` es el único motivo del FALLA formal; está registrada
  como tarea aparte (`task-clasificar-workbench-demo-en-contracts-identity-toml-...`) y el
  coordinador ya autorizó commitear con esa puerta en rojo mientras exista.
- `mark()` solo reescribe el archivo si el modelo tiene algún namespace con baseline (si no hay
  claves, no hay nada que marcar); el comportamiento observable de `names()` no cambia.
