PASA

# Tester deskops-t-35c6f2d4111e: límites de código limpio

Task: `task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo`

Commit del ejecutor: `6fd0a971a65943c0a5151d25b0700c524acc95f1` — *Split five files to meet clean-code limits* (con `Task-Id` de la tarea).
HEAD al probar: `6fd0a971`; `src/`, `contracts/` y `tests/` sin cambios posteriores.

## Veredicto

PASA. `tests/test_clean_code_rules.py` pasa entero sin tocar límites y los tests de las cuatro tareas siguen verdes sin cambios de asserts.

`bash tools/check.sh --fast` sale con rc 1 **solo** por la puerta `identidad` (`workbench_demo`, directorio versionado sin clasificar). Es la excepción autorizada explícitamente por esta tarea («todas las puertas en verde salvo 'identidad' por workbench_demo (excepción autorizada; decisión aparte)»), preexistente y ajena al commit: el commit solo toca los cinco archivos y sus módulos nuevos, no `contracts/identity.toml` ni `workbench_demo`. Las demás puertas pasan (`núcleo aislado`, `capas`, `ejes`, `superficie`).

## Archivos del commit revisados

- `src/sldb/api/rules/rule_graph.py` + `src/sldb/api/rules/rule_view.py` (nuevo)
- `src/sldb/api/rules/rules_on_write.py`
- `src/sldb/api/notations/component_spec_graph.py` + `src/sldb/api/notations/component_spec_build.py` (nuevo)
- `src/sldb/api/stores/store_check.py` + `src/sldb/api/stores/store_check_summary.py` (nuevo)
- `src/sldb/store/diagnostics.py` + `src/sldb/store/diagnostics_models/verdict_notes.py` (nuevo)

Los cuatro módulos nuevos caen dentro de ejes ya declarados (`api/rules` → reglas; `api/notations` → vistas; `api/stores` y `store/diagnostics_models` → op_almacen), así que no hacía falta declararlos en `contracts/layers.toml`. `check_layers` y `check_axes` pasan.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`, `-p no:cacheprovider`)

Base: `/workspace/sldb/.venv/bin/python -m pytest -q` (Python 3.13). `/tmp/ws-venv` no existía en el contenedor; se usó el `.venv` real del repo.

| Archivo | Resultado |
|---|---|
| `tests/test_clean_code_rules.py` (validación de la tarea) | **1232 passed** |
| `tests/api/test_on_write_entering.py` | **8 passed** |
| `tests/api/test_rules.py` | **14 passed** |
| `tests/matching/test_matching_refs.py` | **11 passed** |
| `tests/notations/test_notations_from_graph_cli.py` | **9 passed** |
| `tests/store/test_diagnostics.py` | **17 passed** |
| `tests/notations/test_component_spec_graph.py` (módulo tocado) | **16 passed** |
| `tests/api/test_rules_linked_reach.py` (módulo tocado: rule_graph) | **4 passed** |
| `tests/api/test_structural_noise.py` (módulo tocado: store_check) | **15 passed** |
| `tests/store/test_contract_in_model_node.py` (módulo tocado: store_check) | **13 passed** |
| `tests/test_cli_reconciliation.py` (superficie stores check) | **3 passed** |
| `tests/api/test_gitignore_policy.py` (superficie stores check) | **9 passed** |

No se corrió la suite completa; la corre integrate en el host, según la instrucción del rol.

## Gate rápido

    PATH=/workspace/sldb/.venv/bin:$PATH bash tools/check.sh --fast  -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

La única falla es la excepción autorizada por la tarea; no hay otra puerta en rojo y el commit no introduce la violación.

## Comprobación contra el Goal

- `rule_graph.py` delega la vista declarada y el documento no indexado en `rule_view.py`.
- `rules_on_write.py` parte `check_on_write` en `_write_findings` y `_settle`, conservando orden y comportamiento.
- `component_spec_graph.py` delega los pasos 2-6 en `component_spec_build.py`.
- `store_check.py` delega el resumen/clasificación en `store_check_summary.py`.
- `diagnostics.py` delega campos cambiados, nota y contrato en `verdict_notes.py`.
- Los tests de las cuatro tareas y los de los módulos tocados pasan sin modificar sus asserts.
