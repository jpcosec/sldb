---
id: task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6
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

# Separar el store en un paquete propio (espera la decisión 6)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261018-150534-suggestion-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261018-150534-suggestion-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Mitad de la entrada del drawer task-extract-store-into-generic-typed-document-engine-document-codec-plugins que espera la decisión 6 del dueño: mover sldb.store a un paquete propio (un motor genérico de documentos tipados que consumen sldb, deskops, knowledge y repopackage), o quedarse con el desacople interno. La otra mitad, el desacople interno, está hecha (beb8a99c04, task-desacoplar-el-store-dentro-de-sldb): el store depende del resto de sldb solo por store/exceptions.py, store/runtime_codec.py y store/model_contract.py, así que separarlo reemplaza esas tres costuras. Spec: docs/architecture/store-extraction-proposal.md. Pendiente de la extracción: excepciones propias del store (hoy reexporta las de sldb.core), un codec y un contrato de modelo inyectados en vez de importados, y un paquete con su pyproject y su propia suite.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
