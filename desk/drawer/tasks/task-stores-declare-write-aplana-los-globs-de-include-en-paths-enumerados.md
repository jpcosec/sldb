---
id: task-stores-declare-write-aplana-los-globs-de-include-en-paths-enumerados
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

# stores declare --write aplana los globs de include: en paths enumerados

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261029-005556-unclear-stores-declare-write-aplana-los-globs-de-include-en-paths-enumerados.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261029-005556-unclear-stores-declare-write-aplana-los-globs-de-include-en-paths-enumerados.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

sldb stores declare --write reescribe la sección include: del store.yaml convirtiendo cada 'glob: desk/atoms/atom-*.md' en una lista 'paths:' enumerada (93 líneas nuevas en deskops/.sldb/store.yaml). La declaración es autorada: el glob es la intención del dueño y la enumeración es derivada. Esperado: declare --write conserva los globs y solo agrega lo que falta (links, modelos nuevos), o avisa que va a aplanar y pide confirmación. Reproducción: cd deskops && sldb stores add ../sldb/.sldb --name sldb --store .sldb && sldb stores declare --store .sldb --write && git diff .sldb/store.yaml. Contexto: armando el store central de deskops (links a sldb, spec2viz, pron, scion) el 2026-10-29; restauré el archivo y agregué los links a mano.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
