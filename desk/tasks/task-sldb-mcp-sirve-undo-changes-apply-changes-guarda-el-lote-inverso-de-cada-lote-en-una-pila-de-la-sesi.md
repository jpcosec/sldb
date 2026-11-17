---
sldb:
  by: agent
  at: '2026-11-17T01:34:47Z'
  authority: generated
  via: create_document
id: task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-184421-unclear-ir04b-undo-changes-lo-sirve-sldb-mcp-o-es-una-extensi-n-de-specir-qui-n-guarda-la-pila-de-lotes-inversos-de-la-sesi-n.md
depends_on: []
pills: []
files:
- src/sldb/mcp/write/apply.py
- src/sldb/mcp/write/pending.py
- src/sldb/mcp/signals/catalog.py
- tests/mcp/test_write_tools.py
- docs/architecture/mcp.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
---

# sldb mcp sirve undo_changes: apply_changes guarda el lote inverso de cada lote en una pila de la sesión y undo_changes lo aplica con guardas (IR04b)

## Rationale

_Explain why this task exists or the business driver behind it._

apply_batch ya devuelve report.inverse (83c60239). src/sldb/mcp/signals/catalog.py dice que undo_changes es de sldb y se registra cuando exista; src/sldb/mcp/write/pending.py lo declara no servido; apply_changes (src/sldb/mcp/write/apply.py) no guarda el inverso. IR pregunta quién sirve undo_changes y dónde vive la pila; decisión del coordinador de sldb, siguiendo el catálogo: lo sirve sldb mcp y la pila vive en la sesión del servidor. Origen: desk/inbox/20261116-184421-unclear-ir04b-undo-changes-lo-sirve-sldb-mcp-o-es-una-extensi-n-de-specir-qui-n-guarda-la-pila-de-lotes-inversos-de-la-sesi-n.md.

## Goal

_Describe the concrete result this task must produce._

En una sesión de sldb mcp, cada apply_changes exitoso apila su report.inverse; undo_changes deshace el último lote aplicado (o los N últimos) aplicando su inverso con apply_batch, con las mismas guardas: si alguien escribió entre medio, se rechaza con ConflictError sin escritura parcial y el lote queda en la pila.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) la pila de lotes inversos en el estado de la sesión del servidor mcp (por sesión, en memoria, sin persistir), con push en apply_changes tras un apply exitoso; (2) la tool undo_changes con argumento opcional steps (default 1), que aplica los inversos del más reciente al más antiguo y devuelve lo deshecho; un fallo deja la pila como estaba desde ese lote; (3) quitar undo_changes de pending y del catálogo de no servidos; (4) dry-run si las demás tools de escritura lo tienen; (5) tests en tests/mcp/test_write_tools.py: aplicar, deshacer y comparar el store; deshacer tras una escritura ajena da conflicto y no escribe; deshacer con la pila vacía da un error claro. CHANGELOG y docs/architecture/mcp.md. No entra: persistir la pila entre sesiones, redo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/mcp/write/apply.py, pending.py, pendings.py, tools.py, src/sldb/mcp/signals/catalog.py, el estado de sesión del servidor y src/sldb/api/documents/batch_inverse.py. 2) Implementar la pila y la tool en módulos nuevos del paquete sldb.mcp.write si hace falta por la regla de 80 líneas. 3) Tests y docs. 4) Validation (los tests de mcp necesitan el extra mcp).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_signals.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_dry_run.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; undo_changes figura entre las tools servidas; CHANGELOG, docs y commit; aviso a IR (IR04b se reduce a verificarlo desde specIR).
