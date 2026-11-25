FILE:desk/tasks/task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload.md
---
sldb:
  by: agent
  at: '2026-11-16T05:10:14Z'
  authority: generated
  via: save_document_payload
id: task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

Precisiones (preflight-1): verificado en HEAD: save_document_payload llama pin_payload (payload_save.py:46) y, al renderizar, pin_provenance sobre el texto (render_checked en payload_save_steps.py:92); create_document debe llamar a los dos en el mismo orden relativo (pin_payload sobre el payload antes de renderizar, pin_provenance sobre el texto renderizado antes de escribir). Si Transaction.create (transaction.py:79, que llama create de transaction_ops.py:27) usa otro camino que no pasa por create_document, se agrega el mismo pinneo ahí; si pasa por create_document, no hace falta nada más. "Destino trackeado" es un documento que el store tiene en su índice (store_current lo encuentra); anchor_state "intact" es el valor que devuelve la lectura de anclas para un ancla pinneada con el hash actual del destino (lo que ya prueba tests/api/test_doc_anchors.py para save). El alcance incluye los dos: campos de __doc_anchors__ y el from: de procedencia.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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

