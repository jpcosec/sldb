PASA

# Resultado del tester

- **Task**: `task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización`
- **Rol**: tester
- **Run**: `run-deskops-t-492f877ef22e-a2`
- **Commit probado**: `4bd45239b03272d062ab9c5b5ba3f82871f73e6c` (`NodeLookup resuelve un directorio declarado con o sin barra final`), que continúa el trabajo de `6f14a3b5`.
- **Archivos del commit final**: `src/sldb/api/edges/project_graph/node_lookup.py`, `tests/api/test_project_graph.py`, `CHANGELOG.md`.
- **Archivos acumulados de la tarea**: `src/sldb/api/edges/project_graph/declared_target_nodes.py`, `src/sldb/api/edges/project_graph/node_lookup.py`, `tests/api/test_project_graph.py`, `CHANGELOG.md`.

## Veredicto

El Goal se cumple. Un target declarado que es un directorio existente produce un nodo de directorio y no queda en `missing_targets`/`graph missing`, con o sin `/` final. Un directorio inexistente sigue reportándose como missing. No se expande el directorio en un nodo por archivo.

## Validaciones corridas

No existe `/tmp/ws-venv` en este host; se usó el venv del repo (`/workspace/sldb/.venv`), que es el disponible. No se corrió la suite completa.

| Comando | Resultado |
|---|---|
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/api/test_project_graph.py` | **15 passed** (incluye los dos tests nuevos) |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/api/test_project_graph_config.py` | **11 passed** |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/test_clean_code_rules.py` | **1212 passed** |
| `PATH=/workspace/sldb/.venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast` | **TODAS LAS PUERTAS PASAN** (rc 0) |

No existe `tests/test_node_lookup.py` ni `tests/test_declared_target_nodes.py`; la cobertura del módulo tocado está en `tests/api/test_project_graph.py`.

## Comprobación independiente del caso reportado

Se reprodujo `ProjectGraph.extraction()` con un directorio `generated/` existente y un target `nowhere` inexistente, declarados tanto en `target` como en un `ReferenceField`:

| target | reference | edges | missing_targets |
|---|---|---|---|
| `generated` | `generated` | `source_file:generated` | `[]` |
| `generated/` | `generated/` | `source_file:generated` | `[]` |
| `generated` | `generated/` | `source_file:generated` | `[]` |
| `generated/` | `generated` | `source_file:generated` | `[]` |
| `nowhere` | `nowhere/` | — | `[('card:card-x', 'nowhere/')]` |
| `nowhere/` | `nowhere` | — | `[('card:card-x', 'nowhere')]` |

También se verificó que el nodo existente es `source_file:generated` con `file_kind: directory` y `provenance.source_kind: declared_target` (test `test_a_declared_directory_is_a_node_and_a_missing_one_stays_missing`), y que el test de regresión consulta `ProjectGraph(...).extraction().missing_targets` además de los edges.

## Observaciones no bloqueantes

- El test nuevo normaliza con `rstrip("/")` el `target_id` de los missing al comprobar el inexistente; aun así la aserción exige que el directorio inexistente siga en missing, que es lo que pide el Goal.
- El `CHANGELOG.md` describe correctamente el comportamiento corregido: `NodeLookup` normaliza la `/` final igual que el nodo.
