---
id: task-transacci-n-rollback-falla-con-ruledoc-por-sldb-cache-rules-dirty-json-sin-snapshot
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

# transacción: rollback falla con RuleDoc por .sldb_cache/rules/dirty.json sin snapshot

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-transacción-rollback-falla-con-ruledoc-por-sldb-cache-rules-dirty-json-sin-snapshot.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-transacción-rollback-falla-con-ruledoc-por-sldb-cache-rules-dirty-json-sin-snapshot.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

La transacción no sobrevive a un rollback en un store con RuleDoc: RollbackError por .sldb_cache/rules/dirty.json.

Qué pasa: en un store que tiene RuleDoc y un dirty set ya creado (.sldb_cache/rules/dirty.json, que crea rules check / rules_on_check), cada escritura dentro de sldb.api.transaction pasa por rules_on_write, que llama dirty_set.mark_dirty y reescribe dirty.json. Ese archivo no entra en el snapshot de la transacción (TransactionState.remember). Si la transacción falla después, rollback() (api/documents/transaction_state.py:56) restaura lo snapshoteado, pero transaction_paths.unsnapshotted_drift (:60) ve dirty.json cambiado sin snapshot desde el que restaurarlo. Lo cuenta en failed y lanza RollbackError('Rollback incomplete; not restored: .sldb_cache/rules/dirty.json') encadenado al error original, en lugar de dejar pasar el original.

Efecto en deskops: con las reglas de activación de CC32 sembradas en el desk, todo rollback de una escritura compuesta (atoms merge con falla, conflicto de expected_source_hash → mensaje de conflicto de deskops) sale como RollbackError.

Repro (deskops, rama wt/cc32 c9af867e, sobre sldb main 758772c0):
  tests/test_transaction.py::test_merge_failure_at_the_source_write_leaves_desk_and_store_as_they_were
  tests/test_transaction.py::test_a_conflict_inside_a_compound_write_writes_nothing
En deskops main, sin RuleDoc, los dos pasan.

Propuesta (la arregla coord2 de deskops en una tarea chica de sldb, rama wt/rules-dirty-rollback): que la transacción snapshotee el dirty set antes de que mark_dirty lo toque, para que el rollback lo devuelva a como estaba. La alternativa, excluir .sldb_cache/rules de la deriva, esconde estado y no se recomienda.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
