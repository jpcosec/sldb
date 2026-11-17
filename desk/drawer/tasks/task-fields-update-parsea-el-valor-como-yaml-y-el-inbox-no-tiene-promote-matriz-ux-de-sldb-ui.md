---
id: task-fields-update-parsea-el-valor-como-yaml-y-el-inbox-no-tiene-promote-matriz-ux-de-sldb-ui
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

# fields update parsea el valor como YAML y el inbox no tiene promote (matriz UX de sldb-ui)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261116-161013-suggestion-fields-update-parsea-el-valor-como-yaml-y-el-inbox-no-tiene-promote-matriz-ux-de-sldb-ui.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261116-161013-suggestion-fields-update-parsea-el-valor-como-yaml-y-el-inbox-no-tiene-promote-matriz-ux-de-sldb-ui.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Dos hallazgos de la re-medición de la matriz UX de sldb-ui (runs/ux-stress-20261116/, d2cfea2), que caen del lado del CLI: (1) 'sldb fields update docs/<doc>/<field> <valor>' interpreta el valor como YAML, así que un texto con ': ' (p. ej. 'Uno: dos') falla con un error de validación de pydantic; la UI puede citarlo, pero un valor de texto debería poder pasarse literal (por ejemplo con un flag --string o --raw). (2) 'sldb inbox' no tiene promote, lo que corta la cadena C5 (inbox -> documento). Además fields update/append no aceptan --format (ya avisado en la nota 20261116-094415).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
