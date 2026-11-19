Task: task-selfdoc-genera-distinto-la-referencia-de-stores-merge-driver-segun-la-version-de-python-required-del
Title: selfdoc genera distinto la referencia de stores merge-driver según la versión de python (required del argumento files)
Status: active
Current node: ritual-testing
Task type: task.debug
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T09:53:00Z'
  authority: generated
  via: save_document_payload
id: task-selfdoc-genera-distinto-la-referencia-de-stores-merge-driver-segun-la-version-de-python-required-del
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# selfdoc genera distinto la referencia de stores merge-driver según la versión de python (required del argumento files)

## Rationale

_Explain why this task exists or the business driver behind it._

Dos veces (17-11 y 19-11) un ejecutor en un contenedor scion con python 3.12 de uv regeneró knowledge/commands/cmd-sldb-stores-merge-driver.md con required: false para el argumento files, y en el host (python 3.12.3) selfdoc check lo marca selfdoc/changed porque espera required: true. El coordinador lo revirtió las dos veces (c972a252 en deskops no; en sldb 98ae6cc6 y antes en la tarea de --keep).

## Goal

_Describe the concrete result this task must produce._

La referencia que genera selfdoc para un argumento no depende de la versión de python: el valor de 'required' (y cualquier otro campo derivado de argparse que cambie entre versiones) se normaliza o se deriva del parser de forma estable, y selfdoc check da 0 tanto en el host como en el contenedor scion.

## Scope

_State what is in scope and what is out of scope._

Dentro: encontrar dónde selfdoc lee 'required' de argparse (src/sldb/selfdoc o cli/parser), qué diferencia hay entre 3.12.3 y la 3.12 de uv para un posicional con nargs del merge-driver, y normalizarlo con test. Fuera: cambiar el argparse del comando merge-driver salvo que la normalización lo exija.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducir con los dos pythons (host /usr/bin/python3.12 y uv python 3.12 del contenedor) imprimiendo action.required del argumento files de stores merge-driver; p2: normalizar en el lector de selfdoc; p3: test; p4: selfdoc sync en el host y check en 0; quick_gates antes del commit.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src sldb selfdoc check
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

selfdoc sync en el contenedor y en el host produce la misma referencia de merge-driver y selfdoc check da 0 en los dos.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-selfdoc-genera-distinto-la-referencia-de-stores-merge-driver-segun-la-version-de-python-required-del"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
