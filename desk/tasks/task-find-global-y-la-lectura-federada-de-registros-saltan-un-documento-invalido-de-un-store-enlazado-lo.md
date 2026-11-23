---
sldb:
  by: agent
  at: '2026-11-23T01:33:33Z'
  authority: generated
  via: save_document_payload
id: task-find-global-y-la-lectura-federada-de-registros-saltan-un-documento-invalido-de-un-store-enlazado-lo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-194201-suggestion-find-global-se-cae-por-un-documento-inv-lido-en-un-store-enlazado.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# find --global y la lectura federada de registros saltan un documento inválido de un store enlazado, lo informan con su store y siguen

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261120-194201 (Governance, 2026-11-20): Governance enlaza los stores de 14 desks. 'sldb find <término> --global --store .sldb' termina con 'Unexpected: 1 validation error for TaskDoc' porque shared_llm-gateway tiene una tarea incoherente (task-ci-propio-del-gateway: superseded con historial vacío). Un documento inválido en un desk deja ciego al desk que coordina. Sigue igual en origin/main 6ab01b80. iter_search_records (src/sldb/api/records/iter_records.py:15) llama a sldb.store.query.load_runtime_documents sin accepted_only, y un documento que su modelo rechaza aborta toda la carga. El modo tolerante ya existe: accepted_only/rejected en store/query.py y on_invalid='skip' en src/sldb/api/documents/runtime_documents.py desde 4253c7b9.

## Goal

_Describe the concrete result this task must produce._

Con --global, find (y fields query --global y sections find --global, que pasan por la misma lectura) devuelve los resultados de los documentos válidos de todos los stores. Cada documento rechazado sale en un aviso por stderr con su store, su ruta y su modelo; rc 0 si no hubo otro error.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/records/iter_records.py (cargar con accepted_only=True y rejected=[] cuando include_linked es verdadero), el aviso en src/sldb/cli/commands/find.py y en los otros comandos que llaman a iter_search_records con global_scope, y tests en tests/api/ o tests/store/ con dos stores enlazados, uno con un documento que su modelo rechaza. CHANGELOG.md. Fuera: el modo local sin --global, que sigue fallando con el error que nombra la ruta (SLDBValidationError), y cambiar la validación de TaskDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test que reproduce: store A enlaza a B; B tiene un documento que su modelo rechaza; find --global sobre A hoy aborta. 2) iter_search_records usa la carga tolerante con --global y devuelve los rechazados al llamador. 3) find imprime un aviso por rechazado en stderr. 4) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

El test con dos stores pasa: find --global devuelve los documentos válidos de ambos y avisa del rechazado con su store; la suite completa sale rc 0.
