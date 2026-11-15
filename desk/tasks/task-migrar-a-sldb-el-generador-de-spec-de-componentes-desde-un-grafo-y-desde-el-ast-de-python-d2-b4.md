---
sldb:
  by: agent
  at: '2026-11-15T15:53:53Z'
  authority: generated
  via: save_document_payload
id: task-migrar-a-sldb-el-generador-de-spec-de-componentes-desde-un-grafo-y-desde-el-ast-de-python-d2-b4
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Migrar a sldb el generador de spec de componentes desde un grafo y desde el AST de Python (D2, B4)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: lo genérico va a sldb. spec2viz tiene el módulo graph_import (grafo o snapshot a spec de componentes, función component_spec_from_graph) y el generador python_ast (spec desde el AST de Python).

## Goal

_Describe the concrete result this task must produce._

sldb produce un spec de componentes desde un grafo y desde código Python, reutilizando lo que ya tiene.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Primero comparar, y registrar la comparación en el cierre: sldb ya tiene la proyección de grafo (evaluate_projection_view y save_projection_view, que dan nodos y aristas), el inventario sldb.code con PythonSymbolDoc y el grafo de fuente de python (ver el atom del inventario de código como hechos de fuente), y el cargador de snapshot node-link. Para cada función de spec2viz (en graph_import: load_node_link, load_store_index, node_kind, document_ref, component_spec_from_graph; en el generador python_ast: generate_python_ast_spec, write_spec): si sldb ya la cubre, se reutiliza y el generador usa eso; lo que no, se migra. Resultado: una función de sldb.api que devuelve el spec de componentes (modelo de componente de la tarea de modelos de spec) desde un grafo, un snapshot o un árbol de Python, sin duplicar el escaneo AST de sldb.code. Paridad: tests de spec2viz test_graph_import y los de python_ast portados a sldb. spec2viz no se retira (gate IR13). Cubre B4 del brief.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Informe de comparación; generación desde grafo y desde Python con tests portados verdes; ninguna duplicación del escáner de código; suite de a un archivo, tools/check.sh y stores build --check.
