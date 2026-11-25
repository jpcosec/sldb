---
sldb:
  by: agent
  at: '2026-11-25T01:14:50Z'
  authority: generated
  via: create_document
id: task-sldb-serve-ve-altas-cambios-y-bajas-hechos-por-otro-proceso-sin-reiniciar-cache-invalidado-por-firma
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

# sldb serve ve altas, cambios y bajas hechos por otro proceso sin reiniciar (cache invalidado por firma del store)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 4 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

El cache de sldb serve se invalida cuando cambia la firma del store (mtime o hash de los shards), asi una alta, cambio o baja hecha por la API de Python con serve arriba aparece en la siguiente lectura.

## Scope

_State what is in scope and what is out of scope._

El cache del servidor en src/sldb/cli/serve/ y un test. Fuera: lectura tolerante, Tipo/nombre, 422.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: serve arriba, alta por sldb.api, /graph la muestra sin reiniciar; idem cambio y baja. 2) Firma del store e invalidacion. Correr solo el test nuevo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_cache_externo.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo de alta, cambio y baja externos pasa sin reiniciar serve.
