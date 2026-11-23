---
sldb:
  by: agent
  at: '2026-11-23T01:37:04Z'
  authority: generated
  via: save_document_payload
id: task-load-runtime-documents-informa-los-modelos-que-no-pudo-resolver-en-vez-de-omitirlos-en-silencio
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-212548-suggestion-sldb-api-load-runtime-documents-omite-en-silencio-los-modelos-que-no-resuelven.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# load_runtime_documents informa los modelos que no pudo resolver en vez de omitirlos en silencio

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261120-212548 (IR, cierre de IR04b, 2026-11-20): load_runtime_documents salta sin aviso los modelos que no resuelve. En el store de prueba de IR, los modelos heredados de deskops (model_ref deskops.models...) no resuelven hasta que algo los importa: la misma llamada devuelve 53 documentos al principio y 506 después de una escritura en el mismo proceso. Sigue en origin/main 6ab01b80: _resolve_model_type (src/sldb/store/query.py) traga toda excepción y devuelve None, y _load_one hace 'continue'. Hay una tarea relacionada, task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar. Esa tarea guarda el error de import por modelo para el mensaje de docs show, pero no cambia lo que devuelve load_runtime_documents.

## Goal

_Describe the concrete result this task must produce._

load_runtime_documents(..., on_invalid='skip') devuelve en RuntimeDocuments también los modelos que no resolvió: modelo, store y excepción original. Con on_invalid='raise' emite un warnings.warn por modelo no resuelto que nombra el model_ref y el store. La lista de documentos no cambia de forma.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/store/query.py (_resolve_model_type y _load_one recogen los modelos no resueltos), src/sldb/api/documents/runtime_documents.py (campo nuevo en RuntimeDocuments y el warning), y tests en tests/api/test_api_documents.py con un modelo cuyo model_ref no importa. CHANGELOG.md. Fuera: aceptar un pythonpath nuevo para resolverlos (ya existe el parámetro pythonpath) y el mensaje de docs show, que es de la tarea relacionada.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: store con un modelo cuyo model_ref apunta a un módulo inexistente; on_invalid='skip' lo devuelve como no resuelto y on_invalid='raise' emite el warning. 2) Recoger el error en _resolve_model_type sin cambiar su contrato de devolver None. 3) Cuidar la caché (cached_store), para que un modelo no resuelto no quede cacheado como store vacío sin aviso. 4) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q -p no:cacheprovider tests/api/test_api_documents.py
- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa con caché fría y caliente; la suite completa sale rc 0.
