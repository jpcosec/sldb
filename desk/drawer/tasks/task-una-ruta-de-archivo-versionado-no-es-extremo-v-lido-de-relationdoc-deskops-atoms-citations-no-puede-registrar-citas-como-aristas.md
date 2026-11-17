---
id: task-una-ruta-de-archivo-versionado-no-es-extremo-v-lido-de-relationdoc-deskops-atoms-citations-no-puede-registrar-citas-como-aristas
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

# Una ruta de archivo versionado no es extremo válido de RelationDoc: deskops atoms citations no puede registrar citas como aristas

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261116-193112-suggestion-una-ruta-de-archivo-versionado-no-es-extremo-v-lido-de-relationdoc-deskops-atoms-citations-no-puede-registrar-citas-como-aristas.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261116-193112-suggestion-una-ruta-de-archivo-versionado-no-es-extremo-v-lido-de-relationdoc-deskops-atoms-citations-no-puede-registrar-citas-como-aristas.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

deskops 996becef (deskops atoms citations --write) registra cada cita código→átomo como un RelationDoc cited_by con source = ruta del archivo (p. ej. deskops/services/atoms.py) y target = AtomDoc:<id>. sldb las guarda (stores check PASS) pero el índice de aristas las descarta: sldb edges check da '[edges/invalid] relation cite-...: source <ruta> is not a tracked document' por cada una (store/edge_index/resolve.py::_authored), y edges_to(AtomDoc:<id>, cited_by) no devuelve nada. Pedido: un tipo de nodo para archivos versionados (p. ej. file:<path>) válido como extremo de RelationDoc, o la forma que sldb prefiera para colgar una arista de un archivo del repo. Hasta entonces deskops no corre --write en repos reales. Evidencia: runs/subagents/test-deskops-t-38a62e54c041/verdict.md en deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
