---
sldb:
  by: agent
  at: '2026-11-25T01:19:07Z'
  authority: generated
  via: create_document
id: task-los-modelos-de-sldb-declaran-patron-de-ruta-y-cardinalidad-serve-los-expone-por-modelo-y-post-save-c
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

# Los modelos de sldb declaran patron de ruta y cardinalidad, serve los expone por modelo y POST /save create acepta path

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 3 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

Un atributo de clase documentado declara en el modelo el patron de ruta y la cardinalidad; un endpoint de serve los expone por modelo; POST /save con action create acepta path y respeta el patron.

## Scope

_State what is in scope and what is out of scope._

El atributo de modelo (si no existe), el endpoint en src/sldb/cli/serve/, save create con path, y tests. Fuera: segments, surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver si el modelo ya declara algo parecido. 2) Atributo documentado. 3) Endpoint por modelo. 4) create con path. 5) Tests de los tres. Correr solo esos tests.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_modelo_ruta_cardinalidad.py

## Done When

_Name the observable condition that makes the task complete._

Los tests del atributo, del endpoint y de create con path pasan.
