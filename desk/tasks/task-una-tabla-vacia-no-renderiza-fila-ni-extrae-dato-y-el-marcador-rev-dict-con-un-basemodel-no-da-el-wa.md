---
sldb:
  by: agent
  at: '2026-11-25T01:22:41Z'
  authority: generated
  via: create_document
id: task-una-tabla-vacia-no-renderiza-fila-ni-extrae-dato-y-el-marcador-rev-dict-con-un-basemodel-no-da-el-wa
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

# Una tabla vacia no renderiza fila ni extrae dato, y el marcador rev,dict con un BaseModel no da el warning falso

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 3 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

Render y extract de tablas vacias no inventan fila ni dato, y resolver rev,dict sobre un BaseModel no emite el warning falso.

## Scope

_State what is in scope and what is out of scope._

Render/extract de tablas y la resolucion de rev,dict, con tests. Fuera: None, docs create.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test de tabla vacia (render y extract) y test de rev,dict con BaseModel sin warning. 2) Arreglos. Correr solo esos tests.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_tabla_vacia_y_rev_dict.py

## Done When

_Name the observable condition that makes the task complete._

Los tests de tabla vacia y de rev,dict pasan sin warning.
