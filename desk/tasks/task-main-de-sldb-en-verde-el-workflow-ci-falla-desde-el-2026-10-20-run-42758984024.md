---
sldb:
  by: agent
  at: '2026-11-10T07:23:28Z'
  authority: generated
  via: create_document
id: task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# main de sldb en verde: el workflow CI falla desde el 2026-10-20 (run 42758984024)

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de main de sldb no tiene una corrida verde desde el 2026-10-20 (39464199660). Los nodos de grafo-operable y generalizar-desde-deskops se integraron con tests dirigidos. Regla del dueño: un fallo conocido sin tarea no existe.

## Goal

_Describe the concrete result this task must produce._

El workflow CI de sldb (jobs test 3.12/3.13 y store) termina en success sobre main.

## Scope

_State what is in scope and what is out of scope._

Run 42758984024 (c1f41105). Job test, paso 'Structural gates' (tools/check.sh --fast): 24 archivos sin eje (api/rules/*, api/tags/*, api/views/*, core/finding_route.py); 3 modelos sin clasificar en el contrato (doc_anchor_value, rule_doc, transition_attributes); grados de dependencia de las unidades grafo, notacion y nucleo distintos de los declarados. Job store, paso 'Build deskops' store when it declares one': falla (log con SurfaceDoc y RelationDoc de pron). Además hay que correr los pasos que sigan, que el CI no alcanzó: pytest, python -m build, make world, build --check y selfdoc check. Causa raíz escrita por cada fallo antes del arreglo, sin skip ni xfail, y sin relajar los gates estructurales: se clasifica lo que falta.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast
- pytest (un proceso por archivo, TMPDIR=/dev/shm)
- gh run list --repo jpcosec/sldb --branch main --limit 1

## Done When

_Name the observable condition that makes the task complete._

El run de CI sobre el commit de cierre está en success y su URL queda en references; el informe nombra la causa raíz de cada fallo.
