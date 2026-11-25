FILE:desk/tasks/task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e.md
---
sldb:
  by: agent
  at: '2026-11-25T02:27:02Z'
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

Repo: /mnt/ssd/proyectos/SLDB_1/sldb, en el arbol de trabajo de la tarea (no hace falta estar en main). Decision tomada (coordinador, 2026-11-24): workbench_demo/ es ajeno, igual que surface/: un store de demo que usa el tour del workbench de surface, no producto ni autoaplicacion. Cambio unico: agregar en contracts/identity.toml, junto a los [[foreign]] existentes de 'surface' y 'sldb' (mismas cuatro claves), un bloque [[foreign]] con path = "workbench_demo", files = <salida de 'git ls-files workbench_demo | wc -l', hoy 213>, what = "store de demo del workbench de surface (asistente y tour, 562847e2)" y verdict = "datos de demo de surface, no producto ni autoaplicacion; lo usa el tour del workbench". La nota de por que existe es esa clave what/verdict, no un comentario aparte. No tocar tools/check_identity.py salvo que check.sh siga en rojo por la puerta identidad despues del bloque; en ese caso parar y reportar en vez de cambiar la puerta. No mover ni borrar workbench_demo/.

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

contracts/identity.toml tiene el bloque [[foreign]] de workbench_demo con path, files, what y verdict, y bash tools/check.sh --fast sale con rc 0 (la puerta identidad sin violaciones).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

