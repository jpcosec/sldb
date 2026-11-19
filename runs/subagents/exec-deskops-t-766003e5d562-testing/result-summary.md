PASA

# Tester deskops-t-766003e5d562: check_edges y stale de stores enlazados

Task: `task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2`

Commit revisado: `8955eb0461cfd9c197c9e5efc956b03dd48d523b` — `check_edges: clasifica el stale por el store dueño, no por contar ':'`

Archivos del commit:

- `src/sldb/api/edges/check_edges.py`
- `tests/api/test_api_edges.py`
- `CHANGELOG.md`

## Veredicto

**PASA.** `check_edges` ya no separa los stale por `s.count(":") == 2`: obtiene los nombres de los stores enlazados del índice federado y clasifica como `linked_stale` el id cuyo primer segmento es uno de esos nombres con un `Model:nombre` detrás. Un documento propio con `:` en el nombre queda en `stale` y uno de un store enlazado con `:` en el nombre queda en `linked_stale`. Los ids no cambian.

El test de regresión está en `tests/api/test_api_edges.py` (la ruta real del repo; la tarea la nombraba como `tests/test_api_edges.py`): `test_check_edges_tells_own_stale_from_linked_by_owner_not_by_colons`. Verifiqué que **falla en el commit anterior** (`f083664b`) y pasa en `8955eb04`.

## Validación ejecutada (salida completa en `validation.log`)

Se corrieron de a un archivo, con `TMPDIR=/tmp` y el Python del venv del repo (`.venv/bin/python`, 3.13.18; `/tmp/ws-venv` no existe en este entorno):

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider tests/api/test_api_edges.py` | 0 | 17 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_edge_effects.py` | 0 | 21 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_inherit_model.py` | 0 | 14 passed (incluye `linked_stale`) |
| `python -m pytest -q -p no:cacheprovider tests/api/test_composition_edges.py tests/store/test_upgrade_compat.py` | 0 | 12 passed |
| `python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py -k check_edges` | 0 | 1 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

## Reproducción y comprobaciones adicionales

- **Antes del arreglo:** en un worktree de `f083664b` con el test nuevo copiado, el test falla exactamente por el cruce: `report.stale == ['annex:Table:x:y']` y `report.linked_stale == ['Table:p:q']` (esperado `['Table:p:q']` / `['annex:Table:x:y']`).
- **Caché frío y caliente:** con un store enlazado como `annex`, un documento propio `Table:p:q` y uno enlazado `annex:Table:x:y`, ambos stale, las lecturas local→federada→local→federada dan siempre `stale=['Table:p:q']`, `linked_stale=['annex:Table:x:y']` en la federada y `[]` en la local. Tras reconstruir ambos stores, las dos lecturas dan `ok=True` y sin stale.
- **`ok` y `--local`:** con el documento propio al día y solo el enlazado stale, `check_edges(include_linked=True)` da `stale=[]`, `linked_stale=['annex:Table:x:y']`, `ok=True`; `include_linked=False` da `ok=True`. Por CLI, `edges check` sale 0 con el aviso `1 stale, theirs to fix` y `edges check --local` sale 0 con `Edges OK`.

## Notas

- `stores build --check` no forma parte de las puertas que el encargo de testing manda correr antes del veredicto. No se usó para el veredicto: en el árbol compartido excede los 15 minutos porque `git ls-files --others` arrastra los cientos de artefactos no versionados de `runs/subagents/`, y en un worktree limpio reclama el link `deskops` ausente. Queda para el cierre en el árbol principal.
