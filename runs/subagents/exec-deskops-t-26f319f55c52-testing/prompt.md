Task: task-undo-changes-de-sldb-mcp-el-guard-stale-compara-contenido-sin-procedencia-y-steps-n-no-escribe-nada
Title: undo_changes de sldb mcp: el guard stale compara contenido sin procedencia y steps=N no escribe nada si rechaza un paso
Status: active
Current node: ritual-testing
Task type: task.debug
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-18T23:33:08Z'
  authority: generated
  via: save_document_payload
id: task-undo-changes-de-sldb-mcp-el-guard-stale-compara-contenido-sin-procedencia-y-steps-n-no-escribe-nada
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
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

Ubicaciones (sldb en el HEAD local al despachar): la pila es UndoStack en src/sldb/mcp/write/undo.py (undo_changes y _undo_last, con rejected('stale', ...) en la línea 48). El guard del inverso lo pone _undo en src/sldb/api/documents/batch_inverse.py (líneas 51-52: undo['expected_source_hash'] = source_hash del documento rastreado, que incluye la procedencia). apply_batch en src/sldb/api/documents/apply_batch.py chequea los guards y escribe bajo store_lock(location.store_path, wait=True) (línea 55), todo o nada. Hoy el docstring de UndoStack.undo_changes documenta a propósito el comportamiento parcial ('what was undone stays undone'); esta tarea lo cambia a atómico. La evidencia de IR está en /mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-674fcb14989b-a2/ (result-summary.md, undo-run3.log) y /mnt/ssd/proyectos/SLDB_1/IR/tests/test_mcp_undo.py (sin commit en IR). p1: dos tests nuevos en tests/mcp que fallen antes: (a) inverso guardado, cambio ajeno por api.apply_batch y reversión al contenido anterior, y después undo_changes debe aplicar (hoy da stale); (b) dos lotes donde el segundo edita un documento del primero; undo_changes(steps=2) con un rechazo forzado en el más viejo debe responder written: False y dejar el store y la pila como estaban. p2 (guard): el guard del inverso compara el contenido sin el bloque de procedencia. No hay hoy una función de hash de contenido de documento (api/views/view_revision.content_hash es de vistas), así que se crea una sola en src/sldb/api/documents (hash del payload sin el bloque sldb de procedencia); el inverso guarda ese valor y apply_batch lo chequea como guard nuevo ('expected_content_hash'), sin cambiar expected_source_hash para los demás llamadores. p3 (steps=N): encadenar los N inversos, del más nuevo al más viejo, en una sola llamada a apply_batch, que ya es todo o nada bajo un cerrojo, y sacarlos de la pila solo si se aplicó. Con el guard de contenido, cada inverso más viejo espera el contenido que deja el más nuevo. p4: docs/architecture/mcp.md (la sección de undo) y el docstring de undo_changes documentan el contrato 'mismo contenido salvo procedencia' y el todo o nada de steps; CHANGELOG. p5: el ejecutor corre solo tests/mcp y los tests de los archivos que toque; la suite completa (pytest -n 4 y sldb selfdoc check) la corre integrate. p6: después de su commit con Task-Id, avisa a IR con: deskops message send --root /mnt/ssd/proyectos/SLDB_1/sldb --to IR --kind suggestion --title 'sldb: undo_changes con guard de contenido y steps atómico (IR04b)' '<sha corto del commit, qué cambió y el contrato>'.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/mcp

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos fallan antes y pasan después, la suite completa de sldb pasa (la corre integrate) e IR recibió la nota con el commit.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-undo-changes-de-sldb-mcp-el-guard-stale-compara-contenido-sin-procedencia-y-steps-n-no-escribe-nada"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
