---
id: task-stores-build-check-falla-con-un-store-enlazado-ausente-build-no
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

# stores build --check falla con un store enlazado ausente; build no

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-stores-build-check-falla-con-un-store-enlazado-ausente-build-no.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-stores-build-check-falla-con-un-store-enlazado-ausente-build-no.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

sldb stores build --check falla cuando falta un store enlazado; build no.

En el CI de deskops (run 42751372686 y la reproducción en un clon limpio de deskops wt/main-en-verde-2 7bd88006), .sldb/store.yaml declara links a ../sldb, ../spec2viz, ../pron y ../scion (desde 1b89114c). Esos repos no están al lado en el runner.
- sldb stores build pasa: el store_index versionado ya trae los links, así que apply_links no llama a link_store.
- sldb stores build --check falla con «No store at ../sldb/.sldb»: reconstruye una copia sin .sldb/core, apply_links llama a link_store por cada link y _check_other_exists lanza SLDBStoreError (src/sldb/api/stores/link_store.py:50).

Decisión del coordinador de proyecto (revisable): un store enlazado ausente es alerta, no error. Nombra el link y la ruta, para que en local no se esconda un link roto de verdad.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
