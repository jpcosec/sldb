---
id: task-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo
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

# docs show sobre un store enlazado reporta 'Unknown document target' cuando lo que falla es importar el modelo

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261029-014629-unclear-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261029-014629-unclear-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desde el store central de deskops (links a ../sldb/.sldb), 'sldb docs show sldb:ArchitectureNarrativeDoc/arch-code-docstring-indexing --store .sldb' responde 'Unknown document target' mientras 'sldb docs exists' con el mismo target responde ok. La causa real es que el modelo del store enlazado (docs.models:ArchitectureNarrativeDoc, path docs/models.py relativo a la raíz de sldb) no se puede importar sin --pythonpath ../sldb; con --pythonpath ../sldb el show funciona. El error de import se traga y se reporta como target desconocido: eso es una alerta silenciosa. Esperado: (a) el mensaje distingue 'documento no existe' de 'no pude importar el modelo X del store enlazado Y (pythonpath?)', y (b) idealmente el store enlazado aporta su propio pythonpath (la raíz del proyecto del link) sin que el llamador lo adivine. Reproducción 2026-10-29: cd deskops && sldb docs show 'sldb:ArchitectureNarrativeDoc/arch-code-docstring-indexing' --store .sldb

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
