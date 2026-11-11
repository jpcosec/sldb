---
id: task-h9-run-view-no-encuentra-una-viewdoc-de-un-store-enlazado-unknown-view-bloquea-cc34-de-deskops-da4
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

# H9: run_view no encuentra una ViewDoc de un store enlazado ('Unknown view'); bloquea CC34 de deskops (DA4)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-h9-run-view-no-encuentra-una-viewdoc-de-un-store-enlazado-unknown-view-bloquea-cc34-de-deskops-da4.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-h9-run-view-no-encuentra-una-viewdoc-de-un-store-enlazado-unknown-view-bloquea-cc34-de-deskops-da4.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por CC34 de deskops (worker cc34, 2026-11-11), probado con sldb 1c3132aa. Un store que enlaza a otro store que trackea la ViewDoc da 'Unknown view' en run_view, y por lo tanto en sldb serve GET /views/<x>. Dos causas: (1) el índice compuesto nombra el nodo enlazado '<link>:ViewDoc:<name>' (por ejemplo 'lib:ViewDoc:board') y load_view busca 'ViewDoc:<name>'; (2) read_view resuelve semantics.path contra el project_root local, no contra el root del store enlazado. Consecuencia: la decisión DA4 de deskops (ViewDoc solo como semillas del paquete, sin desk/views/, encontradas por el store de deskops enlazado) no funciona en ningún desk que no sea el propio repo deskops. Esperado: load_view resuelve una ViewDoc de un store enlazado (prueba '<link>:ViewDoc:<name>' cuando no hay local, o por nombre calificado) y lee su archivo desde el root del store que la trackea. Test: un store A que enlaza a B con la ViewDoc en B; run_view(A, 'board') la encuentra y la evalúa sobre los documentos de A.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
