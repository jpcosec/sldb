---
sldb:
  by: agent
  at: '2026-11-16T16:28:54Z'
  authority: generated
  via: save_document_payload
id: task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444
pills: []
files:
- src/sldb/api/documents/apply_batch.py
- src/sldb/api/documents/batch_report.py
- tests/api/test_transaction.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# apply_batch devuelve el lote inverso con guardas: deshacer es de sldb (inbox 20261115-123855)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: deshacer es de sldb, no de los consumidores (specIR, deskops, la UI).

## Goal

_Describe the concrete result this task must produce._

BatchReport lleva el lote inverso, en la forma que acepta apply_batch; deshacer = apply_batch(report.inverse).

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-123855. Crear X se invierte en borrar X; actualizar en restaurar campos o texto previos; borrar en recrear con el contenido previo; aristas igual sobre sus RelationDoc. Cada operación del inverso lleva expected_source_hash del estado que dejó el lote, así que aplicarlo tras un cambio ajeno se rechaza como ConflictError sin escritura parcial. Procedencia del inverso registrada como cualquier escritura. Decidir si se apoya en los snapshots que Transaction ya tiene para el rollback (pregunta de la nota). Cuando esté, la tool undo_changes del MCP de sldb (tarea sldb mcp) lo expone.

Precisiones (coordinador, 2026-11-16): el inverso se arma con payloads, no con bytes: un documento canónico (el render de su payload) vuelve byte a byte; la procedencia del front matter (sldb.by/at/via) puede cambiar y no cuenta para 'igual'. Si el inverso de un delete encuentra el documento recreado por otro, el rechazo es el SLDBStoreError 'already exists' de la prevalidación, que se documenta como conflicto. Esta tarea depende de la tarea de guardas bajo el cerrojo (022444), que debe estar cerrada antes: el inverso se arma dentro de su lock.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) BatchReport (src/sldb/api/documents/batch_report.py) gana inverse: list[dict] = []. 2) Un módulo nuevo batch_inverse.py en el paquete sldb.api.documents con before(...) que, dentro del lock y antes de la transacción, guarda por cambio el modelo, la ruta, current_payload (de batch_prevalidate) y el source_hash del documento existente; e inverse(...) que, después de la transacción y todavía bajo el lock, arma el lote inverso: create -> delete con expected_source_hash del estado nuevo; update -> update con el payload previo completo y expected_source_hash nuevo; delete -> create con el payload, modelo y ruta previos; move -> move de vuelta con hash nuevo; track <-> untrack. 3) apply_batch (src/sldb/api/documents/apply_batch.py) devuelve BatchReport(saved, inverse) con ese inverso, sin pasar de 10 líneas de lógica; prevalidate_changes sigue siendo nombre de módulo en apply_batch.py (el test del lock lo parchea); batch_prevalidate.py está en 80 líneas y no crece. 4) Tests en tests/api/test_transaction.py: aplicar un lote de create+update+delete y después apply_batch(report.inverse) deja payloads, entradas del índice y bytes de los documentos canónicos iguales a los previos; tocar un documento entre medio hace que el inverso se rechace con ConflictError y sin escritura parcial.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los dos tests nuevos; deshacer = apply_batch(report.inverse) deja el store como antes (payloads e índice iguales; bytes iguales para documentos canónicos); CHANGELOG y commit; aviso a IR anotado en result-summary.md.
