Task: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s
Title: El generador del golden de D2 deja de importar spec2viz, para que el retiro de spec2viz no cuente a sldb como consumidor
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
  at: '2026-11-21T02:33:17Z'
  authority: generated
  via: save_document_payload
id: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El generador del golden de D2 deja de importar spec2viz, para que el retiro de spec2viz no cuente a sldb como consumidor

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: 'specir retirement check' de IR (gate final IR13) cuenta una sola dependencia de spec2viz en sldb: runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5 ('from spec2viz.generators import python_ast'). Es el script que congeló el oráculo de D2 en un golden (ce0bd384), y el acta de retiro de IR (docs/spec2viz/acta-de-retiro.md, punto 1 de 'Lo que falta') espera que sldb lo resuelva y responda con el commit.

## Goal

_Describe the concrete result this task must produce._

runs/subagents/20261116-exec-oraculo-d2/gen_golden.py ya no importa spec2viz: o se borra (el golden ya está commiteado en ce0bd384 y el script no lo usa ningún test), o se deja un README en esa carpeta que diga cómo se generó, sin el import. Después, el desk de IR recibe un aviso con el commit, con deskops message send --to IR.

## Scope

_State what is in scope and what is out of scope._

Dentro: runs/subagents/20261116-exec-oraculo-d2/gen_golden.py (borrarlo, con git rm) y, si hace falta, un README.md en la misma carpeta. Fuera: el golden y los tests de D2.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: 'grep -rn gen_golden' en src y tests para confirmar que nada lo usa. p2: 'git rm' del script, y un README.md de 3 líneas en la carpeta que diga que generó el golden de ce0bd384 a partir de spec2viz y que se retiró por el retiro de spec2viz. p3: 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_component_spec_python.py' en verde. p4: commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_component_spec_python.py

## Done When

_Name the observable condition that makes the task complete._

El script no existe o no importa spec2viz; el test de D2 pasa.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
