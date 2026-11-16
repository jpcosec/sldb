# Resultado: executor deskops-e-146155e482b3

Tarea: `task-docs-track-force-sobre-un-documento-ya-trackeado-en-la-misma-ruta-lo-re-indexa-desde-el-archivo-en-l`
Veredicto: **LISTO 0**. Validation pasa entera. `make world` de pron da rc 0 contra este sldb en un clon limpio de pron, siempre que el clon esté en un layout donde resuelva el enlace a deskops (ver §4). El mismo clon contra el HEAD de sldb reproduce el error del CI.

## 1. Cambios (archivo y función)

- `src/sldb/store/ops.py`
  - `StoreOperations.track(..., force=False)`: calcula la ruta relativa primero y llama `_pre_check` con ella y con `force` dos veces, antes de leer el archivo y de nuevo bajo `store_lock`. El re-chequeo bajo cerrojo antes estaba dentro de `_do_track`.
  - `StoreOperations._pre_check(store_path, rel_path, model_entry, doc_name, force=False)`: lee el shard con `load_document_shard`. Si existe y no hay force, lanza `SLDBStoreError("Doc '<n>' already tracked.")`, que es el mensaje de hoy. Si existe y el `path` del shard no es la ruta pedida, lanza `SLDBStoreError("Doc '<n>' already tracked at '<shard>', not '<pedida>'; use move.")`, que nombra las dos rutas.
  - `StoreOperations._do_track`: ya no llama `_pre_check`, porque ahora lo hace `track` bajo el cerrojo. Con force y la misma ruta, re-indexa reescribiendo el shard con hashes del texto actual, más `documents_hash.note`, el resumen del modelo, los índices semántico, de secciones y de aristas, y `cascade_store_hash`. Es el mismo camino de un primer track, así que el documento queda como si se trackeara por primera vez (aclaración 3).
  - `track_document(..., force=False)`: pasa `force`.
- `src/sldb/api/documents/track_document_file.py`
  - `track_document_file` y `_track`: pasan `force` a `track_document`. force sigue saltando el round-trip (`_refuse_unfit`) y además re-indexa (aclaración 2).
  - Docstring: `force` describe el re-index y `Raises` incluye already tracked sin force y la otra ruta.
- `src/sldb/cli/parsers/docs1.py` (`_track`): ayuda de `--force` para `docs track`. **Fuera de la lista de archivos del contrato, pero lo autoriza el Scope (4)**: "ayuda de docs track".
- `tests/api/test_api_documents.py`: helpers `_retrack` e `_index_state`, y 4 tests:
  - `test_track_force_reindexes_a_document_already_tracked_at_the_same_path`: edita el archivo y re-trackea con force; el payload es el nuevo y `check_store(...)["ok"]`.
  - `test_track_without_force_still_refuses_a_document_already_tracked`
  - `test_track_force_refuses_a_document_tracked_at_another_path_and_names_both`: el documento original no cambia.
  - `test_track_force_twice_without_changes_is_idempotent`: escribe un `store.yaml` con `declare_store` (la fixture no tiene uno). Tras dos re-tracks, los shards e índices `.yaml` quedan byte a byte iguales y `store.yaml` no se reescribe ni duplica `login.md`; `check_store` ok.
- `CHANGELOG.md`: entrada en 0.1.13.

`declare_tracked` no se tocó. Ya era idempotente: si `(model, path, name)` ya está declarado, retorna sin guardar (aclaración 4), y el test lo cubre.

Re-index de ediciones externas (aclaración 3): el camino actual es `update_store_indexes` / `StoreIndexRefresh`, que rehashea todo el store. Para un solo documento el cálculo es el mismo que el de `_do_track` (hash de fuente, de contenido y de campos, procedencia, y luego rebuild de los índices derivados), así que reutilicé `_do_track` en vez de refrescar el store entero. `docs track --glob` sigue saltando los ya trackeados, porque filtra antes de llamar.

## 2. Done When

| Punto | Estado |
|---|---|
| Comandos de Validation pasan con los tests nuevos | Sí, los 6 con rc 0 (§3, `validation.log`). |
| `make world` de pron con rc 0 contra este sldb en un clon limpio | Sí, en el layout donde resuelve el enlace a deskops (§4). En `/dev/shm/ci2-pron` literal da rc 2 por el enlace, no por track. |
| CHANGELOG | Hecho. |
| Commit | No: lo hace el coordinador (aclaración 6). |
| Aviso a sldb-ui y pron | No: lo manda el coordinador (aclaración 6). |

## 3. Comandos corridos (salida completa en `validation.log`)

Todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`:

| Comando | Resultado | rc |
|---|---|---|
| `pytest -q tests/api/test_api_documents.py` | 17 passed | 0 |
| `pytest -q tests/api/test_on_write_entering.py` | 7 passed | 0 |
| `pytest -q tests/api/test_api_stores.py` | 12 passed | 0 |
| `pytest -q tests/test_links_batch_cli.py` | 5 passed | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 1177 passed | 0 |
| `bash tools/check.sh --fast` | — | 0 |

No corrí la suite completa ni `stores build --check`; Validation no los pide.

## 4. Reproducción de pron

pron master `39ea972`, deskops (`jpcosec/opsys`) `ee9bc3cd`. Venv con `uv venv` y `uv pip install -e sldb[code,mcp] -e pron[mcp]`, más `-e deskops` en los layouts B y C. Se corrió `make world PYTHON=<venv>/bin/python` con el `bin` del venv en PATH.

**A. Layout pedido (`/dev/shm/ci2-pron`), sldb con el parche: rc 2.** `init --world` (Makefile:31) pasa, sin ningún "already tracked". Falla `pron docs` (Makefile:32):
```
FileNotFoundError: No store_index.yaml at /herramientas/deskops/.sldb
make: *** [Makefile:32: world] Error 1
```
Causa: `pron/.sldb/store.yaml` enlaza `deskops` en `path: ../../../herramientas/deskops/.sldb`, que se resuelve desde la raíz del proyecto. Desde `/dev/shm/ci2-pron` eso es `/herramientas`. Log: `pron-world-ci2-pron.log`.

**B. Layout donde el enlace resuelve (`/dev/shm/ci2-lay/proyectos/PRON/pron` + `/dev/shm/ci2-lay/herramientas/deskops`), sldb con el parche: rc 0.**
```
test -f .sldb/core/store_index.yaml || sldb stores init
/dev/shm/ci2-venv/bin/python -m pron.cli.main init --world . --pythonpath . --knowledge > /dev/null
Sections rebuild: 15 documents missing on disk (RelationTypeDoc: 15); ...
... (lista de RelationDoc, "Skipped missing documents: reltype-...")
rc=0
```
Log completo: `pron-world-layout-fixed.log`.

**C. Mismo layout B, sldb en HEAD `12e9b191` sin el parche (vía `git archive`): rc 2.** Es el error del CI:
```
  File ".../sldb/store/ops.py", line 37, in _pre_check
    raise SLDBStoreError(f"Doc '{doc_name}' already tracked.")
sldb.core.exceptions.sldb_store_error.SLDBStoreError: Doc 'rt-implements' already tracked.
make: *** [Makefile:31: world] Error 1
rc=2
```
Log: `pron-world-layout-head.log`.

Al terminar borré todo lo de `/dev/shm/ci2-*`.

## 5. Desvíos y dudas

- **Probable siguiente fallo del CI (fuera de alcance: no entra cambiar pron ni el CI).** En el job `store` de `.github/workflows/ci.yml`, pron está en `$GITHUB_WORKSPACE/pron` y deskops en `$GITHUB_WORKSPACE/deskops`. El enlace `../../../herramientas/deskops/.sldb` de pron no resuelve ahí, así que tras este arreglo es probable que el CI pase el paso de init y caiga en el de `pron docs` con el `FileNotFoundError` del caso A. Hay que arreglarlo en pron (enlace) o en el CI (layout). Lo dejo al coordinador.
- `src/sldb/cli/parsers/docs1.py` se tocó por el Scope (4) aunque no está en `files:`.
- No hubo pills que leer (`pills: []`).

## 6. Archivos tocados

- `src/sldb/store/ops.py`
- `src/sldb/api/documents/track_document_file.py`
- `src/sldb/cli/parsers/docs1.py`
- `tests/api/test_api_documents.py`
- `CHANGELOG.md`
- Entrega: `runs/subagents/20261116-exec-ci2/{validation.log,result-summary.md,pron-world-ci2-pron.log,pron-world-layout-fixed.log,pron-world-layout-head.log}`
