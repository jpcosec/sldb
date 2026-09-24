---
id: task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido
current_node: checklist-task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido-execution-ready
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido-execution-ready
- checklist-task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido-testing-ready
- checklist-task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Retirar cli/graph y cli/graph_old: copias fosiles de un refactor interrumpido

## Rationale

_Explain why this task exists or the business driver behind it._

Dos refactors simultaneos (commit 73e4553) dejaron tres arboles del mismo concepto. El que gano es cli/graph_ops/ (22 importadores, p.ej. commands/find.py:3, api/search.py:43-49). cli/graph/ no tiene __init__.py y cero importadores. cli/graph_old/__init__.py:3-5 importa .query/.search/.ast_target que no existen: 'import sldb.cli.graph_old' lanza ModuleNotFoundError. Nadie lo noto porque nadie los importa.

## Goal

_Describe the concrete result this task must produce._

Borrar src/sldb/cli/graph/ (6 modulos, 134 lineas) y src/sldb/cli/graph_old/ (4 modulos, 79 lineas), dejando cli/graph_ops/ como unico arbol.

## Scope

_State what is in scope and what is out of scope._

IN: borrar los dos arboles muertos. OUT: NO tocar cli/graph_ops/ (es el vivo), no tocar store/graph/ (esa es la capa de grafo, otra cosa distinta).

## Implementation Path

_Outline the expected implementation route or affected surface._

Censo AST de importadores sobre src/ y tests/ para confirmar cero uso de ambos. Verificar con diff -r que graph/ y graph_old/ son copias de lo que graph_ops/ ya hace. Borrar ambos arboles.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

pytest completo en 1015 passed 0 failed; los directorios cli/graph/ y cli/graph_old/ no existen; cli/graph_ops/ intacto.
