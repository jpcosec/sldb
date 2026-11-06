---
id: task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload
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

# Cambiar __indexed__ de un modelo no marca stale la proyeccion del payload

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgo de GO04 (d7eefdeb, hipotesis H1): la firma de contrato del shard (contract_signature) cubre {fields, references, containment, compositions} como fija el contrato de GO04, pero no __indexed__. Un documento ya indexado conserva la proyeccion vieja hasta que su shard se reconstruye (cambio de texto o stores build). Propuesta: agregar indexed (nombres de __indexed__ ordenados, lista vacia si falta) a la firma, en GO05 o en un nodo propio del plan grafo-operable, con test: cambiar __indexed__ marca stale y la reconstruccion reproyecta.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
