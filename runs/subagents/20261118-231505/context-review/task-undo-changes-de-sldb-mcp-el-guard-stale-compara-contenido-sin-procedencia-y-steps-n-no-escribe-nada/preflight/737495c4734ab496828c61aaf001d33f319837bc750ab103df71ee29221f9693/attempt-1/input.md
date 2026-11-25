FILE:desk/tasks/task-undo-changes-de-sldb-mcp-el-guard-stale-compara-contenido-sin-procedencia-y-steps-n-no-escribe-nada.md
---
sldb:
  by: agent
  at: '2026-11-18T23:14:20Z'
  authority: generated
  via: create_document
id: task-undo-changes-de-sldb-mcp-el-guard-stale-compara-contenido-sin-procedencia-y-steps-n-no-escribe-nada
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# undo_changes de sldb mcp: el guard stale compara contenido sin procedencia y steps=N no escribe nada si rechaza un paso

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261117-135338-suggestion-ir04b-undo-changes-de-sldb-mcp-falla-tras-re-sellar-procedencia-stale-imposible-de-satisfacer-steps-2-escribe-a-medias de IR (IR04b, evidencia en IR/runs/subagents/deskops-e-674fcb14989b-a2/: result-summary.md, undo-run3.log y tests/test_mcp_undo.py en el árbol de IR, sin commit). Probado con un cliente MCP real sobre una copia del store, undo_changes (d0ee07a3) cumple los niveles, pero: (2) el guard stale compara source_hash, que incluye la procedencia re-sellada (sldb.at, via), así que después de un cambio ajeno y su reversión al contenido anterior el lote queda en rejected: stale para siempre y atascado en la pila; (3) con dos lotes donde el segundo edita un documento del primero, undo_changes(steps=2) responde applied: False, rejected: stale, written: True, es decir que escribió el inverso del segundo y rechazó el primero. IR04b está bloqueada esperando esto.

## Goal

_Describe the concrete result this task must produce._

(1) El contrato de undo queda documentado como 'mismo contenido salvo procedencia': deshacer es una escritura nueva y re-sella sldb.at, via y los hashes derivados. (2) El guard stale de undo compara el contenido del documento sin el bloque de procedencia, así que un documento que volvió al contenido esperado ya no queda stale. (3) undo_changes(steps=N) valida la cadena entera antes de escribir: cada paso se compara contra el estado que dejaría el paso anterior y, si alguno se rechaza, no se escribe nada (written: False) y la pila queda intacta.

## Scope

_State what is in scope and what is out of scope._

Dentro: el código de undo_changes de sldb mcp y la pila de lotes inversos de apply_batch (src/sldb/mcp y src/sldb/api, donde están el guard y la pila), sus tests, el CHANGELOG y la documentación del contrato de undo. Fuera: cambiar el formato de la procedencia o el source_hash del índice; specIR (IR04b relaja su validación según el contrato documentado).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducir los dos defectos en tests del repo, primero fallando: (a) un lote que se deshace después de un cambio ajeno revertido al contenido esperado; (b) dos lotes encadenados y steps=2, que hoy escriben a medias. Basarse en IR/tests/test_mcp_undo.py y en undo-run3.log, citando archivo y línea del guard y de la pila. p2: el guard compara un hash del contenido sin procedencia (reutilizar la función de sldb que ya calcula el hash de contenido si existe; si no, una sola función nueva). p3: steps=N valida todos los pasos en memoria, encadenando el estado esperado, antes de la primera escritura, y escribe bajo el cerrojo del store. p4: documentar el contrato de undo ('mismo contenido salvo procedencia') donde está la doc de undo_changes, y CHANGELOG. p5: avisar a IR por deskops message send con el commit, para que IR04b siga.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/mcp

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos fallan antes y pasan después, la suite completa de sldb pasa (la corre integrate) e IR recibió la nota con el commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-undo-changes-de-sldb-mcp-el-guard-stale-compara-contenido-sin-procedencia-y-steps-n-no-escribe-nada: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

