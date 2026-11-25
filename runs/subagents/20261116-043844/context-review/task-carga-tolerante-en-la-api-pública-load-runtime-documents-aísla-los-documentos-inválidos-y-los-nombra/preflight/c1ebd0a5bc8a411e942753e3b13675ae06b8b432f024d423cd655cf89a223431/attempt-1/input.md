FILE:desk/tasks/task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra.md
---
sldb:
  by: agent
  at: '2026-11-16T04:06:49Z'
  authority: generated
  via: create_document
id: task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261031-033714-suggestion-resiliencia-en-carga-de-store-ante-documentos-invalidos-y-problems-estructurados.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/runtime_documents.py
- src/sldb/store/edge_index/edge_index.py
- tests/api/test_api_documents.py
- tests/api/test_api_edges.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
---

# Carga tolerante en la API pública: load_runtime_documents aísla los documentos inválidos y los nombra, y EdgeIndex expone problemas estructurados

## Rationale

_Explain why this task exists or the business driver behind it._

En la integración del Workspace de graph_ui, load_runtime_documents abortó con ValidationError para todo el store porque un solo Markdown era inválido, sin nombrar el archivo culpable. El modo que salta documentos rechazados existe pero es interno (accepted_only en src/sldb/store/query.py:75-88, lo usa stores check); el envoltorio público src/sldb/api/documents/runtime_documents.py:17 no lo expone. EdgeIndex.problems es list[str] (src/sldb/store/edge_index/edge_index.py:18), así que un consumidor tiene que parsear texto. Origen: desk/inbox/20261031-033714-suggestion-resiliencia-en-carga-de-store-ante-documentos-invalidos-y-problems-estructurados.md.

## Goal

_Describe the concrete result this task must produce._

load_runtime_documents(..., on_invalid="skip") devuelve los documentos sanos y una lista de (ruta, modelo, error) de los inválidos sin lanzar; el comportamiento por defecto (on_invalid="raise") no cambia salvo que el mensaje nombra la ruta del documento; EdgeIndex gana un campo problem_details con objetos {kind, document, detail} junto a problems, que no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: parámetro on_invalid: Literal["raise", "skip"] = "raise" en la función pública de src/sldb/api/documents/runtime_documents.py, implementado con accepted_only de src/sldb/store/query.py; un tipo de retorno para el modo skip (dataclass RuntimeDocuments con documents e invalid) definido en el mismo módulo y exportado; en modo raise, la excepción incluye la ruta. En EdgeIndex (src/sldb/store/edge_index/edge_index.py) un campo nuevo problem_details: list[EdgeProblem] (modelo pydantic con kind, document, detail), poblado donde hoy se agregan strings a problems; problems sigue igual para no romper consumidores. Tests en tests/api/test_api_documents.py (store con un documento inválido: skip devuelve los sanos y nombra el inválido; raise nombra la ruta) y en tests/api/test_api_edges.py (problem_details tiene la misma cantidad que problems). CHANGELOG.md. No entra: resolve_runtime_doc focalizado sin barrido total (src/sldb/api/records/resolve.py:6) — se mide en esta tarea y se anota el tiempo en el informe, pero su cambio es otra tarea si hace falta; quitar problems; tocar graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/documents/runtime_documents.py, src/sldb/store/query.py (75-88), src/sldb/store/edge_index/edge_index.py y grep "problems.append\|problems=" en src/sldb/store/edge_index. 2) Implementar on_invalid. 3) Agregar EdgeProblem y problem_details en cada punto donde se agrega un problema. 4) Tests. 5) stores build --check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los tests nuevos; on_invalid="skip" sobre un store con un documento inválido devuelve los sanos y el inválido en invalid; problem_details existe y cuadra con problems; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

