Task: task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid
Title: La escritura por campos (save_document_payload y el update de apply_batch) falla nombrando el contenido que se perdería en vez de borrarlo en silencio
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T07:50:24Z'
  authority: generated
  via: save_document_payload
id: task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261116-223438-suggestion-save-document-payload-y-apply-batch-update-borran-en-silencio-contenido-que-el-modelo-no-declara-ws47-del-drawer-de-deskops.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/payload_save.py
- src/sldb/api/documents/payload_save_steps.py
- tests/api/test_structural_noise.py
- tests/api/test_transaction.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La escritura por campos (save_document_payload y el update de apply_batch) falla nombrando el contenido que se perdería en vez de borrarlo en silencio

## Rationale

_Explain why this task exists or the business driver behind it._

save_document_payload, y el update de apply_batch que pasa por él, re-renderiza el documento desde el payload sin mirar el archivo previo; refuse_structural_noise y refuse_undeclared_frontmatter solo se aplican al crear o trackear. Si el archivo trae ruido estructural o frontmatter que el modelo no declara, una escritura por campos lo borra sin aviso. graph_ui va a escribir por apply_batch update. Origen: desk/inbox/20261116-223438-suggestion-save-document-payload-y-apply-batch-update-borran-en-silencio-contenido-que-el-modelo-no-declara-ws47-del-drawer-de-deskops.md.

## Goal

_Describe the concrete result this task must produce._

Una escritura por campos sobre un documento cuyo archivo actual tiene ruido estructural o frontmatter no declarado falla antes de escribir, con un error que nombra lo que se perdería, y deja el archivo intacto; los documentos limpios se escriben igual que hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: aplicar la misma guarda que al crear (refuse_structural_noise y refuse_undeclared_frontmatter sobre el texto actual del archivo) en el camino de save_document_payload (src/sldb/api/documents/payload_save.py y payload_save_steps.py) antes de re-renderizar, con el mismo tipo de excepción; tests en tests/api/test_structural_noise.py y en tests/api/test_transaction.py (apply_batch update sobre un archivo con frontmatter extra falla sin escritura parcial). CHANGELOG. No entra: un modo force para estas escrituras.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer payload_save.py, payload_save_steps.py, refuse_structural_noise.py, frontmatter_keys.py y transaction_ops.py. 2) Agregar la guarda. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_structural_noise.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a deskops y graph_ui.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
