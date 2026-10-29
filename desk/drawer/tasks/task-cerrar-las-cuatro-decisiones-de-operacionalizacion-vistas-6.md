---
id: task-cerrar-las-cuatro-decisiones-de-operacionalizacion-vistas-6
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

# Cerrar las cuatro decisiones de OPERACIONALIZACION-VISTAS §6

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261001-031224-suggestion-cerrar-las-cuatro-decisiones-de-operacionalizacion-vistas-6.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261001-031224-suggestion-cerrar-las-cuatro-decisiones-de-operacionalizacion-vistas-6.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Tomarlas como decididas según su recomendación y llevarlas a código: (1) offsets del ancla sobre el campo body del átomo, no sobre el render canónico (requiere source_field); (2) valor descartado en status, no borrar; (3) prosa generada con marca generado y hash de los átomos de origen, desactualizada si el hash cambia, nunca reescrita sola; (4) extractor externo a la UI y a /extract/segments que escribe AtomDoc con status propuesto y nunca toca confirmado. Conviene hacerlo después de fijar el set bootstrap porque las cuatro tocan AtomDoc.

## Avance (2026-10-18)

(1) `source_field` (default `body`) y (2) `descartado` en `status` ya están en surface/dev/atoms-store/models.py y en levira-store (152fc723). Faltan (3) la prosa generada con marca y hash de los átomos de origen y (4) el extractor externo; quedan bloqueadas por 20261001-031225 (átomo y field).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
