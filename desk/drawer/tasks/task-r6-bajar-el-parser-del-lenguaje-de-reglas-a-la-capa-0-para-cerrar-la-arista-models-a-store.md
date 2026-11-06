---
id: task-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store
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

# R6: bajar el parser del lenguaje de reglas a la capa 0 para cerrar la arista models a store

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgo de GO06 (622da0b5): RuleDoc valida con validadores pydantic que condition, where y subject parseen (principio del dueno), y el parser vive en store/graph/language; el import es diferido y quedo declarado como [allow].upward [models, store] y [[pending]] R6 en contracts/layers.toml. Reparacion: bajar tokenizador y parser (sin evaluador ni vista de grafo) a la capa 0 junto con WherePredicateError, que el almacen los reexporte (como StoreError en R2), quitar la entrada upward y el pending R6, con check_layers en PASS.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
