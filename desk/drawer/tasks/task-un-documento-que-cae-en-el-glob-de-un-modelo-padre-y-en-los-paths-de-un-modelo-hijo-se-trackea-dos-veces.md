---
id: task-un-documento-que-cae-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-dos-veces
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Un documento que cae en el glob de un modelo padre y en los paths de un modelo hijo se trackea dos veces

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-un-documento-que-cae-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-dos-v.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-un-documento-que-cae-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-dos-v.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Visto en deskops el 2026-11-10 con sldb@main. El .sldb/store.yaml de deskops declara TaskDoc con el glob desk/tasks/task-*.md (desde 376fdcce) y además los paths explícitos de TaskCodeDoc y TaskDebugDoc, que son hijos de TaskDoc. sldb stores build trackea los 5 tasks dos veces: bajo su modelo hijo y otra vez bajo TaskDoc. sldb stores build --check da rc 0 igual, y los selectores por nombre quedan ambiguos porque el mismo id resuelve a dos documentos.

Además, sldb stores declare --write conserva el glob autorado, y no hay CLI para quitar una entrada include de store.yaml. Editar .sldb a mano está prohibido, así que el desk no puede corregirse solo.

Esperado: (a) cuando un archivo cae en el glob de un modelo y en los paths de un descendiente, gana el modelo más específico y se trackea una sola vez, o build --check lo marca como error (store/duplicate-tracking); (b) una vía de CLI para quitar o reemplazar una entrada include (sldb stores undeclare o declare --write con --drop-glob). Tarea consumidora en el drawer de deskops: quitar o migrar el glob TaskDoc cuando exista la vía.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
