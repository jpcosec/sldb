Task: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa
Title: sldb docs create -o resuelve la ruta contra el cwd (o avisa)
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
  at: '2026-11-25T05:41:19Z'
  authority: generated
  via: save_document_payload
id: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
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

Contrato elegido: sldb docs create -o <ruta relativa> resuelve la ruta contra el directorio actual del proceso (no contra la raiz del store) y escribe ahi.

## Scope

_State what is in scope and what is out of scope._

El comando docs create y un test. Fuera: render y fields.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Encontrar docs create en src/sldb/cli/ (grep -rn 'def.*create' src/sldb/cli/ | grep -i doc). 2) Test NUEVO tests/test_docs_create_output_path.py: store temporal, cwd = un subdirectorio del proyecto, docs create -o sub.md -> el archivo queda en <cwd>/sub.md. 3) Arreglo. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs_create_output_path.py

## Done When

_Name the observable condition that makes the task complete._

El test de docs create -o relativa pasa.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-79041272f6a9"

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
