---
sldb:
  by: agent
  at: '2026-11-17T15:02:32Z'
  authority: generated
  via: save_document_payload
id: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
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
