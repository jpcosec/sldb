---
id: task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci
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

# python-sync no destrackea un PythonSymbolDoc cuyo símbolo desapareció

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-símbolo-desapareció.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-símbolo-desapareció.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

python-sync / stores build no destrackean un PythonSymbolDoc cuyo símbolo desapareció del código.

Hallazgo de la tarea main de sldb en verde (sci-worker): el paso del CI «sldb stores build» en sitio da undeclared: 108, todas knowledge/symbols/python-sldb-*.md. Son PythonSymbolDoc que versionó la migración 9bc591c3 (2026-11-04), de símbolos que c420809c borró al retirar el journal (journal.record, _track_and_record, _save_and_record, ...). Ninguno existe en el código actual. python-sync no destrackea un PythonSymbolDoc de su system cuyo símbolo ya no está, y apply_declaration.undeclared (api/stores/apply_declaration.py:75) marca la fila trackeada que ningún include ni derived cubre. build --check pasa porque construye una copia desde cero.

Arreglo inmediato, en la tarea del CI: destrackear las 108 con la CLI (sldb docs untrack), como en e1805fc6. Esta nota pide el arreglo de producto: que python-sync (o stores build) destrackee los PythonSymbolDoc de su system cuyo símbolo ya no existe, para que no vuelva a pasar. Cambia la semántica (borra documentos trackeados derivados) y necesita un test.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
