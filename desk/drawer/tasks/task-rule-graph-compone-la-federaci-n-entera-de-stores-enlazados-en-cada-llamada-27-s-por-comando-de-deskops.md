---
id: task-rule-graph-compone-la-federaci-n-entera-de-stores-enlazados-en-cada-llamada-27-s-por-comando-de-deskops
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

# rule_graph compone la federación entera de stores enlazados en cada llamada (27 s por comando de deskops)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-rule-graph-compone-la-federación-entera-de-stores-enlazados-en-cada-llamada-27-s-por-comando-de-desk.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-rule-graph-compone-la-federación-entera-de-stores-enlazados-en-cada-llamada-27-s-por-comando-de-desk.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

rule_graph compone la federación entera de stores enlazados en cada llamada: unos 27 s por comando de deskops.

Medición de perf-worker (deskops, rama wt/perf-cli, informe runs/subagents/perf-worker-report.md 7cf821f3; datos crudos en coord2-ccconfig/perf/):
- sldb.api.rules.rule_graph (src/sldb/api/rules/rule_graph.py:84) llama a load_edge_index(store, True). Eso compone los 7 stores enlazados del desk de deskops (unos 28 927 nodos, 159 433 aristas, unos 9 600 shards yaml con deepcopy; live_stale rehashea todo) para evaluar las reglas de 21 documentos locales.
- load_edge_index(include_linked=False) tarda 0,27 s (521 nodos, 993 aristas). Con include_linked=True, 27,09 s en frío y 3,15 s en caliente.
- En deskops, rule_graph corre una vez por comando (dos en advance: holding+blocked y on_write). Así, deskops show/next/advance pasaron de 1,1-1,4 s antes de CC32 a 29-35 s en main, y add task de 1,35 s a 30 s (on_write del Board por transaction.update).
- Efecto: test_activation_rules y test_lifecycle_end_to_end ya no entran en timeout 900, y el CI de deskops tiene timeouts en los tests con advance/show/next/add task.

Pedido: que la evaluación de reglas (on_write, on_transition, edges_holding/edges_blocked y rules check/explain) no componga la federación entera cuando las reglas solo leen documentos locales y sus vecinos. Los findings tienen que quedar idénticos.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
