Task: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest
Title: Limpieza de cáscaras vacías de la API y de los residuos de kgdb (graph parser, help_texts_graph, ingest_sldb, python_source_graph)
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T12:43:20Z'
  authority: generated
  via: save_document_payload
id: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files:
- src/sldb/cli/parsers/graph.py
- src/sldb/cli/parsers/stores.py
- src/sldb/cli/commands/help_texts_graph.py
- src/sldb/store/graph/ingest_sldb.py
- src/sldb/selfdoc/python_source_graph.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Limpieza de cáscaras vacías de la API y de los residuos de kgdb (graph parser, help_texts_graph, ingest_sldb, python_source_graph)

## Rationale

_Explain why this task exists or the business driver behind it._

Quedan residuos de kgdb y cáscaras vacías: src/sldb/cli/parsers/graph.py, src/sldb/cli/parsers/stores.py (partes), src/sldb/cli/commands/help_texts_graph.py, src/sldb/store/graph/ingest_sldb.py y src/sldb/selfdoc/python_source_graph.py, además de módulos de la API que solo reexportan o no hacen nada. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Cada uno de esos archivos y cada cáscara vacía de sldb.api queda borrado si nada lo usa, o reducido a lo que se usa, sin cambiar ningún comportamiento observable (CLI, API pública, tests).

## Scope

_State what is in scope and what is out of scope._

Entra: para cada archivo nombrado y cada módulo de src/sldb/api que no tenga lógica propia, buscar usuarios (grep de imports, entrada del CLI, selfdoc) y borrarlo o reducirlo; mantener la API pública declarada en los __all__; anotar en result-summary.md cada archivo con su decisión y su evidencia. CHANGELOG. No entra: cambiar comandos del CLI ni la API pública.

Precisiones (coordinador, bundle-1): cáscara = módulo de src/sldb/api cuyo cuerpo solo tiene docstring, imports, reexports o __all__. Uso = cualquier import o referencia por nombre en src/, tests/, tools/, docs/ o en los entry points de pyproject.toml. Un módulo usado solo para reexportar parte de la API pública declarada en un __all__ se conserva. No se retira ningún subcomando del CLI; en src/sldb/cli/parsers/stores.py solo salen funciones o constantes sin uso. result-summary.md del run-dir lleva la tabla archivo -> borrado|reducido|conservado con la evidencia de grep.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario con grep. 2) Borrar o reducir uno a uno, corriendo los tests de su vecindad. 3) Validation. 4) Informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_backend.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md tiene la tabla archivo -> borrado, reducido o conservado (evidencia); CHANGELOG y commit.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
