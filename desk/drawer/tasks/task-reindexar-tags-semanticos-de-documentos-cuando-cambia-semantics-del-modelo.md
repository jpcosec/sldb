---
id: task-reindexar-tags-semanticos-de-documentos-cuando-cambia-semantics-del-modelo
status: deferred
summary: ''
tags:
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

# Reindexar tags semanticos de documentos cuando cambia __semantics__ del modelo

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261124-190859-suggestion-reindexar-tags-semanticos-de-documentos-cuando-cambia-semantics-del-modelo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261124-190859-suggestion-reindexar-tags-semanticos-de-documentos-cuando-cambia-semantics-del-modelo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

El shard semantico de un documento (.sldb_cache/semantic/<Model>/<doc>.yaml) se guarda bajo source_hash: si un modelo suma una semantica en __semantics__ (deskops: TaskDoc suma board.tareas), los documentos ya indexados con el mismo texto conservan el indice viejo. sldb stores update/build, reindex_model y track_document_file(reindex=True) no lo refrescan; solo untrack_document + track_document_file lo hace (untrack borra el shard). Pedido: una operacion en bloque (p.ej. reindex_model(..., semantics=True) o sldb stores update --semantics) que descarte los shards de un modelo cuyo flatten_model_semantics ya no esta contenido en semantic_tags. Mientras tanto deskops tags migrate --apply reindexa por documento con untrack+track.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
