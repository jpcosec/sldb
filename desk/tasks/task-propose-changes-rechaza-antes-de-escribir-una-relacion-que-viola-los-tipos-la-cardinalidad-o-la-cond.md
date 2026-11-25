---
sldb:
  by: agent
  at: '2026-11-25T23:45:02Z'
  authority: generated
  via: save_document_payload
id: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- src/sldb/api/documents/apply_batch.py
- src/sldb/api/documents/batch_edges.py
- src/sldb/api/documents/batch_report.py
- src/sldb/mcp/write/apply.py
- src/sldb/mcp/write/findings.py
- src/sldb/mcp/write/pending.py
- src/sldb/mcp/write/pendings.py
- src/sldb/mcp/write/tools.py
- src/sldb/store/edge_index/doc_kinds.py
- src/sldb/store/edge_index/resolve.py
- tests/mcp/test_write_tools.py
- tests/test_mcp_propose_rejects_invalid_edges.py
- 560e5a1e02fdcadda82224428df3826405bc1045
depends_on: []
pills: []
files:
- src/sldb/api/documents/apply_batch.py
- src/sldb/api/documents/batch_edges.py
- src/sldb/api/documents/batch_report.py
- src/sldb/mcp/write/apply.py
- src/sldb/mcp/write/findings.py
- src/sldb/mcp/write/pending.py
- src/sldb/mcp/write/pendings.py
- src/sldb/mcp/write/tools.py
- src/sldb/store/edge_index/doc_kinds.py
- src/sldb/store/edge_index/resolve.py
- tests/mcp/test_write_tools.py
- tests/test_mcp_propose_rejects_invalid_edges.py
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-propose-changes-rechaza-antes-de-escribir-una-relacion-invalida
---

# propose_changes rechaza antes de escribir una relación que viola los tipos, la cardinalidad o la condición de su tipo de relación

## Rationale

_Explain why this task exists or the business driver behind it._

ADR docs/architecture/pron-is-archived.md (JP, 2026-11-25): pron se archiva y la edición desde una interfaz escribe por sldb. Hoy sldb detecta una relación inválida después de escribirla (sldb.api check_edges), y su propio MCP lo declara como faltante (src/sldb/mcp/write/pendings.py, "the missing edge validation"). Rechazar antes de escribir era lo único que tenía solo pron y que la edición por gestos de graph_ui necesita.

## Goal

_Describe the concrete result this task must produce._

Que proponer un lote que crea o cambia una relación devuelva el rechazo, con un motivo por cada violación, antes de tocar el store; y que el mismo lote completo se prevalide como unidad.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/mcp/write/ (propose, pendings, findings), src/sldb/mcp/changes/assert_edge.py y sldb.api.apply_batch con dry_run, reusando las comprobaciones de tipos, cardinalidad y condición que ya hace check_edges. Fuera: portar código de pron, el registro persistente y deshacer entre sesiones (tarea aparte), cualquier interfaz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero docs/architecture/rules.md, edges.md y mcp.md, y cómo check_edges decide que una relación es inválida. La validación previa usa esas mismas funciones sobre el estado que resultaría del lote; no se escribe un segundo validador.

Aclaraciones de la revisión: Simular sin escribir: aplicar el lote sobre una copia en memoria de los documentos afectados (en el orden del lote; una relación puede apoyarse en otra del mismo lote) y correr sobre ella las mismas funciones de check_edges; si exigen store escrito, extraer la parte pura y que check_edges la siga usando. Hash = el root hash del store (store_index) antes y después: igual. Rechazo = la estructura de rechazo que propose_changes ya devuelve hoy, una entrada por violación con la relación (origen, tipo, destino) y el código de la violación (tipo, cardinalidad o condición). Si apply_batch ya tiene dry_run, devuelve los mismos rechazos; si no lo tiene, no se crea. 'Igual que antes' = mismo valor de retorno y mismas escrituras; los tests existentes de mcp/write siguen pasando. pendings: quitar la entrada que hoy marca la validación de relaciones como faltante. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_mcp_propose_rejects_invalid_edges.py
- python -m pytest -q tests -k "mcp or apply_batch or check_edges"

## Done When

_Name the observable condition that makes the task complete._

Un lote con una relación entre modelos que su RelationTypeDoc no admite, otro que excede la cardinalidad y otro que incumple la condición devuelven cada uno un rechazo que nombra la relación y la violación, y el hash del store no cambia. Un lote válido se comporta igual que antes. Un lote con una relación válida y otra inválida se rechaza entero. pendings deja de informar la validación de relaciones como faltante. apply_batch con dry_run informa lo mismo.
