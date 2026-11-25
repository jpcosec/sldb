---
sldb:
  by: agent
  at: '2026-11-25T01:23:17Z'
  authority: generated
  via: create_document
id: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb docs create -o resuelve la ruta contra el cwd (o avisa)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 3 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

docs create -o con una ruta relativa la resuelve contra el directorio actual, o avisa claramente si la resuelve contra otro lado.

## Scope

_State what is in scope and what is out of scope._

El comando docs create y un test. Fuera: render y fields.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test desde un cwd distinto de la raiz. 2) Arreglo. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs_create_output_path.py

## Done When

_Name the observable condition that makes the task complete._

El test de docs create -o relativa pasa.
