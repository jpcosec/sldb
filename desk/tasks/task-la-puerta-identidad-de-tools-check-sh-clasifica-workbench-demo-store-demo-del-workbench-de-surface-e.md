---
sldb:
  by: agent
  at: '2026-11-25T01:26:51Z'
  authority: generated
  via: save_document_payload
id: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e
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

# La puerta identidad de tools/check.sh clasifica workbench_demo (store demo del workbench de surface) en contracts/identity.toml

## Rationale

_Explain why this task exists or the business driver behind it._

Desde 562847e2 (asistente y tour del workbench) el repo versiona workbench_demo/ en la raiz y contracts/identity.toml no lo clasifica: bash tools/check.sh --fast termina en rc 1 por 'directorio versionado sin clasificar en la raiz: workbench_demo'. Los testers de deskops tratan rc distinto de 0 como FALLA, asi que la puerta falla en todas las tareas de sldb (lector de surface, attach_atom_edges, plan Datalog del 2026-11-23) aunque el cambio no lo toque.

## Goal

_Describe the concrete result this task must produce._

contracts/identity.toml clasifica workbench_demo/ con la categoria que corresponda a un store de demo de la superficie (o la que el contrato prevea para fixtures o demos versionadas), con una nota de por que existe; bash tools/check.sh --fast sale con rc 0 en main.

## Scope

_State what is in scope and what is out of scope._

contracts/identity.toml y, si la puerta lo necesita, tools/check_identity.py y su test. No mover ni borrar workbench_demo/ (lo usa el tour del workbench).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tools/check_identity.py y las categorias de contracts/identity.toml. 2) Clasificar workbench_demo con la categoria existente que encaje; si ninguna encaja, agregar una para demos de superficie con su regla. 3) bash tools/check.sh --fast en 0.

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

bash tools/check.sh --fast rc 0; la clasificacion trae nota de por que existe workbench_demo.
