---
sldb:
  by: agent
  at: '2026-11-25T17:42:06Z'
  authority: generated
  via: create_document
id: task-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior-porque-el-registro-de-movimientos-per
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

# undo_changes deshace un cambio aplicado en una sesión anterior porque el registro de movimientos persiste en el store

## Rationale

_Explain why this task exists or the business driver behind it._

ADR docs/architecture/pron-is-archived.md (JP, 2026-11-25): el registro persistente de movimientos y el deshacer entre sesiones eran de pron y pasan a sldb. Hoy el deshacer del MCP es por sesión y en memoria (src/sldb/mcp/write/undo.py): al reiniciar el servidor se pierde. Una persona que edita desde una interfaz necesita deshacer después de cerrar y volver.

## Goal

_Describe the concrete result this task must produce._

Que cada lote aplicado quede registrado en el store con lo necesario para revertirlo, y que undo_changes funcione desde un proceso distinto del que lo aplicó.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/mcp/write/ (apply, undo) y el registro de escrituras del store. Fuera: portar MoveDoc de pron, las proyecciones de sesión, cualquier interfaz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero docs/architecture/sldb-absorbs-kgdb.md, sección "The write journal belongs to the substrate", y journal-authority.md y transactions.md: el registro de escrituras ya es del sustrato. El deshacer se apoya en él; si le falta algo para revertir un lote, se agrega ahí y no en un registro paralelo.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_mcp_undo_across_sessions.py
- python -m pytest -q tests -k "mcp and undo"

## Done When

_Name the observable condition that makes the task complete._

Se aplica un lote con un servidor, se termina ese proceso, se levanta otro sobre el mismo store y undo_changes restaura el contenido de los documentos y el hash del store al valor anterior al lote. Deshacer dos veces revierte dos lotes en orden inverso. Deshacer un lote cuyo documento cambió después se rechaza con motivo y no escribe nada.
