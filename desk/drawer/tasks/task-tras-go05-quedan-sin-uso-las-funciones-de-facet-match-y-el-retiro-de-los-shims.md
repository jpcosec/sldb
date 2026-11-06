---
id: task-tras-go05-quedan-sin-uso-las-funciones-de-facet-match-y-el-retiro-de-los-shims
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

# Tras GO05 quedan sin uso las funciones de facet_match y el retiro de los shims

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-tras-go05-quedan-sin-uso-las-funciones-de-facet-match-y-el-retiro-de-los-shims.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-tras-go05-quedan-sin-uso-las-funciones-de-facet-match-y-el-retiro-de-los-shims.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgo de GO05 (8be66bde): el ejecutor de StructuredQuery evalua por payload_match.filters_hold y el lenguaje nuevo, asi que en src/sldb/store/graph/facet_match.py quedan sin uso matches_filters, facet_matches, condition_matches y ordered_*. Los shims where_parse/compile_where y FieldCondition (DeprecationWarning) y la traduccion field_condition_translation se retiran en GO10. Esta nota agrupa el codigo muerto que GO10 debe borrar junto con los shims, con test de que nada en src/ los importa.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
