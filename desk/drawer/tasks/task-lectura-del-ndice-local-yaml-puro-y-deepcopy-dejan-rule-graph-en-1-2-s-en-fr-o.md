---
id: task-lectura-del-ndice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-fr-o
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

# lectura del índice local: yaml puro y deepcopy dejan rule_graph en 1-2 s en frío

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-lectura-del-índice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-frío.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-lectura-del-índice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-frío.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Lectura del índice local: yaml puro y deepcopy hacen que rule_graph en frío tarde 1,2-2,1 s en stores grandes, y deskops show task 2,8 s en el desk del repo de deskops.

Residual de la tarea de rule_graph (wt/rule-graph-local bdb9b0ff, informe runs/subagents/rg-worker-report.md). Con las reglas evaluadas sobre el índice local, el tiempo que queda es la lectura de ese índice: carga YAML en Python puro (sin CSafeLoader) y deepcopy en store/io. Mediciones del rg-worker:
- rule_graph en frío: 1,2-2,1 s en stores grandes;
- deskops show task: 2,8 s en el desk del repo de deskops, sin RuleDoc;
- desk nuevo de init: 1,4 s.

Aceptación pedida por el coordinador de proyecto: deskops show task < 2 s en el desk de deskops y rule_graph en frío < 1 s, con findings y salidas idénticas.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
