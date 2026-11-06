---
id: task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura
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

# on_write: alerts sin listener se pierden por la API y la regla ve las aristas previas a la escritura

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgos de GO08 (3af872e7, hipotesis H2 y H3): (1) las alerts de on_write viajan por sldb.core.finding_route y solo la CLI instala alert_sink; un programa que usa sldb.api sin instalar listener no las recibe (propuesta: save_document_payload devuelve tambien los findings de la escritura, o finding_route guarda por defecto y expone una lectura). (2) on_write evalua el payload pinneado pero sigue las aristas del indice anterior a la escritura: una regla con camino sobre un campo que la propia escritura cambia ve el destino viejo (propuesta: componer las aristas salientes del documento desde el payload nuevo antes de evaluar). Tests: uno por caso.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
