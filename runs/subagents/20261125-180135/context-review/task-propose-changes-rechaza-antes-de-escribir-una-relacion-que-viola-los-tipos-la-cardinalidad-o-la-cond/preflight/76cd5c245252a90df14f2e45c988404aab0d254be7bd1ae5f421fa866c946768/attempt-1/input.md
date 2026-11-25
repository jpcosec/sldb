FILE:desk/tasks/task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond.md
---
sldb:
  by: agent
  at: '2026-11-25T17:39:31Z'
  authority: generated
  via: create_document
id: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
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

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_mcp_propose_rejects_invalid_edges.py
- python -m pytest -q tests -k "mcp or apply_batch or check_edges"

## Done When

_Name the observable condition that makes the task complete._

Un lote con una relación entre modelos que su RelationTypeDoc no admite, otro que excede la cardinalidad y otro que incumple la condición devuelven cada uno un rechazo que nombra la relación y la violación, y el hash del store no cambia. Un lote válido se comporta igual que antes. Un lote con una relación válida y otra inválida se rechaza entero. pendings deja de informar la validación de relaciones como faltante. apply_batch con dry_run informa lo mismo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

