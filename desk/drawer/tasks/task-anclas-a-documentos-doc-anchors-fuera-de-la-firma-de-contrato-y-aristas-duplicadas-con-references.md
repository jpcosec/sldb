---
id: task-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references
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

# Anclas a documentos: __doc_anchors__ fuera de la firma de contrato y aristas duplicadas con __references__

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgos de GO07 (4d521da8, hipotesis H4 y H11): (1) agregar o cambiar __doc_anchors__ en un modelo no mueve contract_signature (GO04), asi que los documentos existentes no ganan sus aristas references hasta la proxima reconstruccion; lo mismo con un cambio de __contract__ sin mover los shards (el indice compuesto en cache no lo ve). Va junto con task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload (misma firma). (2) Un campo declarado a la vez en __references__ y en __doc_anchors__ genera aristas duplicadas, y la de __references__ apunta al literal doc:... sin resolver (store/edge_index/declared_references.py). Propuesta: rechazar esa doble declaracion al cargar el modelo (SLDBModelError, como __indexed__) o que __references__ ignore los campos ancla; test de rechazo.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
