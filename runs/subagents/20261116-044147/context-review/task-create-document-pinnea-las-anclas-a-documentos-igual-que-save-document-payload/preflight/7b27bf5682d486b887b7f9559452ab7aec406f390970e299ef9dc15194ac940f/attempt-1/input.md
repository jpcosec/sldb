FILE:desk/tasks/task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload.md
---
sldb:
  by: agent
  at: '2026-11-16T04:08:30Z'
  authority: generated
  via: create_document
id: task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-g-consumer-cumplido-por-deskops-cc32-6afc78b0.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/create_document.py
- tests/api/test_doc_anchors.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# create_document pinnea las anclas a documentos igual que save_document_payload

## Rationale

_Explain why this task exists or the business driver behind it._

GO07 pinnea al guardar: un doc:Model:name sin @sha256 en un campo de __doc_anchors__ o en el from: de procedencia recibe el hash de contrato del destino (src/sldb/api/documents/doc_anchor_pinning.py, pin_payload y pin_provenance). save_document_payload lo hace (src/sldb/api/documents/payload_save.py:46), pero create_document (src/sldb/api/documents/create_document.py) renderiza el payload sin pinnear. Un recibo creado y nunca reescrito queda con anchor_state lost aunque su destino exista; deskops lo esquiva con create + update en la misma transacción (hipótesis H-CC32-2 de deskops CC32). Origen: desk/inbox/inbox-note-g-consumer-cumplido-por-deskops-cc32-6afc78b0.md (hipótesis 2).

## Goal

_Describe the concrete result this task must produce._

Un documento creado con create_document cuyo campo de __doc_anchors__ nombra un destino trackeado sin @sha256 queda escrito con el ancla pinneada (anchor_state intact al leerlo), igual que si se hubiera guardado con save_document_payload.

## Scope

_State what is in scope and what is out of scope._

Entra: en create_document llamar pin_payload(location.store_path, model_type, payload) antes de _rendered (y pin_provenance sobre el texto si save_document_payload también lo hace; seguir exactamente el mismo orden que payload_save.py). Lo mismo dentro de la transacción si create pasa por otro camino (buscar create en src/sldb/api/documents/transaction*.py). Test en tests/api/test_doc_anchors.py: un modelo con __doc_anchors__ y un destino trackeado; create_document deja el valor con @sha256 y el ancla intact; un destino no trackeado deja el valor como estaba (lost), como en save. CHANGELOG.md. No entra: cambiar el testigo de any en los findings (hipótesis 1 de la nota) ni anchors check sobre índices anteriores a GO07 (hipótesis 3).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer payload_save.py (líneas 30-60), doc_anchor_pinning.py, create_document.py y grep -rn "create_document\|def create" src/sldb/api/documents/transaction*.py. 2) Agregar el pinneo en el mismo punto relativo. 3) Tests.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos pasan con el test nuevo; CHANGELOG y commit; aviso a deskops con deskops message send --to deskops de que create ya pinnea (puede quitar su create + update).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

