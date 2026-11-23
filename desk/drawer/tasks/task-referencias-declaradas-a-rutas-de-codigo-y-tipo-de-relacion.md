---
id: task-referencias-declaradas-a-rutas-de-codigo-y-tipo-de-relacion
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

# referencias declaradas a rutas de código y tipo de relación

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261122-185413-suggestion-referencias-declaradas-a-rutas-de-c-digo-y-tipo-de-relaci-n.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261122-185413-suggestion-referencias-declaradas-a-rutas-de-c-digo-y-tipo-de-relaci-n.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de Chatbot_Infra en el triaje del 2026-11-22: es un pedido para sldb que quedó escrito allá con sldb inbox el 2026-11-04 y nunca llegó a este desk. Texto original: PaginaWiki declara __references__ = [relacionadas, fichas, codigo]. Las de relacionadas (Model:nombre) llegan al índice; las de fichas y codigo son rutas de archivos no trackeados y quedan como sldb://unresolved_ref en el shard, pero edges show no las devuelve y no hay un nodo de archivo o de código al que apunten. Además una referencia declarada siempre es relation references con el campo en metadata: para que página->ficha, página->código y página->página sean relaciones tipadas (agrupa_ficha, posee_codigo, relacionada_con, ya registrados como predicados) hay que escribir un RelationDoc por arista (cientos de archivos). Sugerencia: __reference_relations__ = {campo: relation_type} y nodos de archivo para rutas del repo.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
