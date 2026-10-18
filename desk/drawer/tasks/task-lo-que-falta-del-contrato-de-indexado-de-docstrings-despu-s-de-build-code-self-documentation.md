---
id: task-lo-que-falta-del-contrato-de-indexado-de-docstrings-despu-s-de-build-code-self-documentation
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

# Lo que falta del contrato de indexado de docstrings después de build-code-self-documentation

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261018-172014-suggestion-lo-que-falta-del-contrato-de-indexado-de-docstrings-despu-s-de-build-code-self-documentation.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261018-172014-suggestion-lo-que-falta-del-contrato-de-indexado-de-docstrings-despu-s-de-build-code-self-documentation.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Seguimiento de task-build-code-self-documentation: lo que la sección 7 del spec (docs/architecture/code-docstring-indexing.spec.md) pide y todavía no está, después de las tandas A a D del 2026-10-18.
1. Imports bajo condición o TYPE_CHECKING, y shadowing o rebinding de nombres: hoy la resolución es léxica y no los distingue (sección 4.1).
2. Propósito generado desde el primer párrafo del docstring (sección 2): PythonSymbolDoc.purpose sigue siendo un placeholder escrito a mano; hay que migrar reportando las diferencias, sin pisar lo escrito (sección 7).
3. Reportar por separado las declaraciones faltantes, las explicaciones faltantes y los mapeos sin resolver (sección 7); semantic_gaps solo cuenta placeholders.
4. Reconciliación por productor en el store (sección 4): hoy el grafo es un archivo regenerable y no hay aristas tipadas en el edge index.
5. Aislamiento de la herencia de tags entre stores: la herencia ya respeta el alcance del escaneo, pero no hay un test con dos stores.
Ya hecho: inventarios de CLI y Python, procedencia, sincronización incremental, metadata estricta con diagnósticos, herencia léxica de tags con origen, re-exports y la proyección a spec2viz (spec2viz 8207dfe), que valida.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
