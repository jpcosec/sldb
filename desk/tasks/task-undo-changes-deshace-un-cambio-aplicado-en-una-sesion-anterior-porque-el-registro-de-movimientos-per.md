---
sldb:
  by: agent
  at: '2026-11-25T18:13:53Z'
  authority: generated
  via: save_document_payload
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

Aclaraciones de la revisión: Es el mismo artefacto: se extiende el write journal del sustrato (docs/architecture/journal-authority.md y transactions.md de sldb); no se crea un registro paralelo. Cada lote aplicado guarda id de lote, orden, y por documento su before-image y el hash posterior. Conflicto: si el hash actual del documento difiere del hash posterior guardado, se rechaza con motivo. undo_changes sin argumento revierte el último lote no revertido; con id solo si es el último no revertido (si no, rechazo con motivo). Hash del store = hash de los documentos (store_index), sin contar el journal. Un segundo proceso abre el mismo store y deshace (sirve un subprocess en el test). tests/test_mcp_undo_across_sessions.py se crea. Va después de propose-changes (mismo mcp/write): parte de main actual. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_mcp_undo_across_sessions.py
- python -m pytest -q tests -k "mcp and undo"

## Done When

_Name the observable condition that makes the task complete._

Se aplica un lote con un servidor, se termina ese proceso, se levanta otro sobre el mismo store y undo_changes restaura el contenido de los documentos y el hash del store al valor anterior al lote. Deshacer dos veces revierte dos lotes en orden inverso. Deshacer un lote cuyo documento cambió después se rechaza con motivo y no escribe nada.
