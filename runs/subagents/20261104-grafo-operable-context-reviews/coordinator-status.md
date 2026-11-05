# Coordinator status (robocop2) — 2026-11-05

## Nodo GO03 — Costura GraphBackend sobre networkx — SQUASH A MAIN POR EL COORDINADOR

Rama `wt/go03` (worktree `sldb-wt-go03`). Por orden de JP, el coordinador hace el squash a main vía PR con `gh` (cuenta jpcosec). GO04 no se abre hasta que GO03 esté en main.

### Commits de la rama (sobre main local)
Commits de main local que viajan en la rama porque el push a main da **403** (protección de rama); el supervisor decide si entran en el squash o los separa:
- `9d9666a5` driver `context_review.py`: TIMEOUT 1800 s (autorizado por el supervisor).
- `674b2ae0` GO03 promovido con deskops (Board.md, TaskDoc, `.sldb/store.yaml`, store_index, models/BoardDoc, models/TaskDoc, documents/BoardDoc/Board.yaml, documents/TaskDoc/task-go03-….yaml).
- `ab161b34` precisiones p5–p7 tras el cold-bundle (con `deskops edit task`).

Commits del nodo:
- `369021ee` status del bloqueo por timeouts (histórico, este archivo lo reemplaza).
- `5e16f6fa` goldens de los seis comandos graph capturados desde main **antes** de tocar código.
- `8f0e83f6` paquete `src/sldb/store/graph/backend/` con la implementación networkx.
- `55661f06` api/graph y los seis comandos graph enrutan por `backend.analyze`.
- `231be158` clave `graph_backend` en `store.yaml` (ausente = networkx; otro valor = error).
- `709afd23` tests (`tests/store/test_graph_backend.py`, 9 tests).
- `71bec911` `docs/architecture/graph-backend.md` y CHANGELOG.
- `ecdf4e2c` + `3cb940dd`: el ejecutor escribió a mano una sección de hipótesis en el TaskDoc (contra la regla CLI-only, por un prompt mío anterior a ella); la revertí. Neto: la rama **no modifica `desk/`**. Las hipótesis van abajo.
- `1f1f3ac0` corrección tras la suite completa: la resolución de `graph_backend` sale de `sldb.store` (importaba `sldb.api.stores.store_declaration`, rompiendo `tests/test_store_seams.py`). Ahora el store solo tiene `make_backend(name)`; `declared_graph_backend(store_path)` vive en `api/stores/store_declaration.py` y `backend_for(store_path)` en `api/graph/analyze.py`.

### Aceptación línea por línea
| Línea | Evidencia |
|---|---|
| Goldens de los seis comandos graph idénticos a antes | `tests/fixtures/graph_goldens/{path,cycles,order,components,central,similar}.txt` capturados en `5e16f6fa` desde main (argumentos p7); `git diff 5e16f6fa..HEAD -- tests/fixtures/graph_goldens/` vacío; `test_graph_goldens` pasa. |
| Tests existentes de api/graph pasan sin cambios | `git diff main..HEAD -- tests/` solo agrega `tests/fixtures/graph_goldens/*` y `tests/store/test_graph_backend.py`; ningún test existente modificado. `tests/api/test_api_graph_analysis.py` pasa. |
| Backend espía: cada comando graph y cada función de api/graph invocan al backend | `test_every_api_analysis_and_every_cli_command_calls_the_backend` (diez funciones de `analyze.py`, seis subcomandos; p3). |
| Carga del índice compuesto del propio repo | `test_the_repository_composed_index_loads_into_the_backend` (`compose_edge_index(<repo>/.sldb)` → `load(índice, None)`; p2). |
| `has(id) and status != "x"` por eval → finding con forma GO02 | `test_eval_returns_one_finding_with_the_go02_shape` (`node`, `holds`, `clause`, `seen`; p4). |
| Predicado con camino → NotImplementedError | `test_eval_with_a_path_is_not_implemented_yet`; además `test_eval_by_export_id_without_projection_says_so` (ValueError "sin proyección para <id>"). |
| store.yaml sin clave → networkx; clave inválida → mensaje definido | `test_an_absent_graph_backend_key_means_networkx`, `test_explicit_networkx_is_accepted`, `test_another_graph_backend_fails_with_the_defined_message` (`graph_backend <valor> no admitido; admitidos: ["networkx"]`). |
| Protocolo documentado | `docs/architecture/graph-backend.md` (load/eval/analyze, el backend no expone su grafo; motores futuros detrás de la costura). |
| CHANGELOG | entrada en `CHANGELOG.md` (`71bec911`). |

### Verificación
- Nodo (tras `1f1f3ac0`): `tests/test_store_seams.py tests/store/test_graph_backend.py tests/api/test_api_graph_analysis.py tests/test_clean_code_rules.py` → **721 passed**. Siempre con `PYTHONPATH=$PWD/src` (el venv tiene sldb editable apuntando al clon principal).
- Suite completa #1 (antes de `1f1f3ac0`): 1 failed (`test_store_seams::test_nothing_in_the_store_imports_the_layers_above_it`), 1617 passed, 24 skipped, 52 xfailed (los 52 xfail strict de GO02), 59 min. El fallo era de GO03 y se corrigió en `1f1f3ac0`.
- Suite completa #2: **no se corrió hasta el final, a propósito**. JP señaló sobretesteo: `1f1f3ac0` solo mueve dos funciones de módulo y el fallo era un chequeo estático de imports, cubierto por los 721 tests dirigidos. Con load ~25 en 6 núcleos (nueve pytest de otras sesiones en paralelo), la suite iba al 12 % tras una hora. La detuve.
- Gates estructurales (`tools/check.sh --fast`, el paso de CI previo a pytest): main ya está rojo (`persistencia` 35 vs 33, `operacion` 47/45), así que en CI pytest no llega a correr desde al menos el 2026-10-29. GO03 añadía `grafo` needs 4→5 (eval reutiliza `store/query_engine/where_*`, de la unidad `persistencia`). Lo declaré en `contracts/layers.toml` (`needs = 5` con comentario). Con eso la rama da los mismos dos errores que main; `persistencia` pasa de 33 a 34 en el código (sigue declarado 35, desajuste previo).
- Propuesta: suite completa una sola vez por nodo, serializada con `flock ~/.cache/pytest-full.lock`; después de cada corrección, solo los tests dirigidos.

### Desvíos de `files`
- `src/sldb/cli/commands/graph.py` (+4/−1) no está en `files`: `GraphCLI(backend=None)` pasa el backend a `GraphAnalysisCLI` (H5). Necesario para inyectar el espía en los seis subcomandos.
- `src/sldb/api/graph/__init__.py` y `src/sldb/cli/parsers/graph_analysis.py` están en `files` pero no hizo falta tocarlos.

### Hipótesis del ejecutor (regla 6 de alcance.md; no se registran en el TaskDoc por la regla CLI-only hasta que haya comando)
- H1: `eval` recibe el predicado como texto y lo parsea dentro del backend (no hay aún tipo "predicado parseado" público).
- H2: `analyze` admite además `paths`, `layers`, `islands`, `isolated` (las otras funciones de `analyze.py`), aparte de los seis ops del contrato.
- H3: `model <= X` se evalúa con `payload["model"]` y `payload["base_models"]`.
- H4: `eval` sin sujeto recorre la proyección y, con proyección `None` (siempre en GO03), devuelve `[]`. **A revisar en GO04/GO05**: rules-language §6 dice que el dominio sin sujeto es todos los documentos.
- H5: el backend se inyecta en la CLI con `GraphCLI(backend=...)` / `GraphAnalysisCLI(backend=...)`.

### Revisiones en frío
- Preflight (attempt-1, technical_ok): 4 ambigüedades → p1–p4 en el Scope vía `deskops edit task`. El `disposition.md` y la edición de `receipt.json` de GO03-preflight **se escribieron a mano antes de la regla CLI-only**; quedan como están y se rehacen con `deskops review dispose` cuando GC03 se integre.
- Bundle: attempt-1..3 timeouts a 900 s (técnicos, no cuentan); attempt-4 con TIMEOUT 1800, technical_ok, `disposition: pending` en receipt (no lo toco). 3 ambigüedades → p5 (protocolo de tres operaciones: dag manda sobre brief), p6 (`files` manda sobre OUTPUT_SCOPE), p7 (argumentos de los goldens), todas vía `deskops edit task` (`ab161b34`). FUTURO sin hallazgo nuevo.

### Otros pendientes para el supervisor
- **403 al pushear main**: `9d9666a5`, `674b2ae0`, `ab161b34` solo existen en main local y en esta rama.
- **PythonSymbolDoc sin trackear** (202 en el clon `sldb` + `knowledge/symbols/*.md` gitignorados, creados 22:05–22:58 del 2026-11-04): ningún comando mío los generó. Lo más probable: `sldb selfdoc python-sync` o tests de selfdoc corriendo vía el editable install, solapados con la suite de GO02 y los workers pi. No pude confirmarlo. No los commiteé.
- **`documents_count: 5` en `.sldb/core/models/TaskDoc.yaml`** (commiteado en `674b2ae0`) cuenta dos TaskDoc ajenos sin trackear (`task-congelar-journal-…`, `task-el-store-se-parte-…`) que no commiteé; el conteo queda inconsistente con lo trackeado hasta que se commiteen o se borren con `sldb docs delete`.
- El worktree ajeno `sldb-wt-store-split` no lo toqué.
- Push de `wt/go03` con `--force-with-lease` (la rama se rebasó sobre main local después del primer push de `369021ee`).
