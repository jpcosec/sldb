---
id: task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject
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

# Dos formas de serializar un escalar al sustituir llaves: effects de GO09 y where_subject

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgo de GO09 (33b3c7a0, hipotesis H3 y H4): la sustitucion {campo} en sets de effects serializa con yaml.safe_dump (1e20 da 1.0e+20) y cuenta datetime.date como escalar literal, mientras fill_braces/scalar_literal de where_subject usa Decimal sin exponente y no resuelve fechas. Son dos formas de serializar el mismo escalar en sldb. Propuesta: una sola funcion de serializacion de escalares para llaves, usada por where_subject y edge_effects, con tests de numeros grandes, floats, booleanos y fechas.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
