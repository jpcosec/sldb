---
id: task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb
current_node: checklist-task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb-execution-ready
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb-execution-ready
- checklist-task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb-testing-ready
- checklist-task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Retirar core/ingest: isla muerta que sostiene el ciclo kgdb-sldb

## Rationale

_Explain why this task exists or the business driver behind it._

core/ingest/ no tiene ningun importador (grep -rn 'core.ingest' src tests -> vacio) y ademas es inimportable: engine.py:3-8 importa wiki_compiler/ontology, no declarados en pyproject.toml ni instalados. Es el producto anterior. Sus 4 imports 'from kgdb.contracts.node import KnowledgeNode' (scanner.py:5-6, python_scanner.py:4, typescript_scanner.py:3-4) son el unico ciclo sldb->kgdb que queda, y apuntan a un shim que re-exporta un tipo que vive en el propio sldb (sldb/store/graph/node.py:12).

## Goal

_Describe the concrete result this task must produce._

Borrar src/sldb/core/ingest/ completo (9 modulos, 328 lineas) y con ello el ciclo de imports sldb->kgdb.

## Scope

_State what is in scope and what is out of scope._

IN: borrar src/sldb/core/ingest/ y cualquier referencia colgante. OUT: no tocar selfdoc/python_scanner.py (ese es el scanner VIVO), no tocar los shims de kgdb, no tocar store/.

## Implementation Path

_Outline the expected implementation route or affected surface._

Verificar cero importadores con censo AST sobre src/ y tests/ (no solo grep de la definicion). Borrar el arbol. Confirmar que no queda ningun 'from kgdb' en src/sldb/ salvo el test de paridad tests/api/test_api_graph.py:78-81, que usa importorskip y es intencional.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

pytest completo en 1015 passed 0 failed; 'grep -rn "from kgdb\|import kgdb" src/sldb/' sin resultados; el arbol core/ingest/ ya no existe.
