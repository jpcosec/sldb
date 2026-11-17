---
sldb:
  by: agent
  at: '2026-11-17T11:18:28Z'
  authority: generated
  via: create_document
id: task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-080455-suggestion-docs-track-force-re-indexa-sin-validar-pedido-de-un-re-index-que-valide.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/track_document_file.py
- src/sldb/store/ops.py
- src/sldb/cli/parsers/docs1.py
- tests/api/test_api_documents.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
---

# docs track --reindex re-indexa un documento ya trackeado validándolo, sin saltar el round-trip como --force

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, docs track --force sobre un documento ya trackeado devuelve rc 0 aunque el archivo no valide (enum inválido, frontmatter YAML roto) y queda indexado; después docs show falla. Es lo que dice el contrato: --force salta el round-trip. Por eso la UI guarda con untrack + track (5,5-6,2 s contra 4-5 s). Origen: desk/inbox/20261117-080455-suggestion-docs-track-force-re-indexa-sin-validar-pedido-de-un-re-index-que-valide.md.

## Goal

_Describe the concrete result this task must produce._

docs track --reindex (y track_document_file(..., reindex=True)) re-indexa desde el archivo un documento ya trackeado en la misma ruta, como --force, pero corre las mismas validaciones que un track normal: si el archivo no valida falla con el error de validación y deja el índice como estaba. --force no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: el flag --reindex en el parser y el comando de docs track, el parámetro reindex en track_document_file (src/sldb/api/documents/track_document_file.py) y su paso hasta StoreOperations.track (src/sldb/store/ops.py); --reindex y --force juntos se rechazan con un error claro; tests en tests/api/test_api_documents.py: reindex de un archivo válido editado deja el payload nuevo, de uno inválido falla y no cambia el índice, sobre un documento no trackeado se comporta como track. CHANGELOG y ayuda. No entra: cambiar --force.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer track_document_file.py, ops.py (camino de force de la tarea CI2) y el parser de docs track. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a sldb-ui.
