Task: task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta
Title: El merge driver de sldb se instala solo al preparar un store y stores check avisa si falta
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
  at: '2026-11-20T07:13:17Z'
  authority: generated
  via: save_document_payload
id: task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El merge driver de sldb se instala solo al preparar un store y stores check avisa si falta

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de inbox 20261119-154109-suggestion-el-merge-driver-de-sldb-deber-a-instalarse-solo-al-preparar-un-store (pedido de JP, 2026-11-19). install_merge_driver (src/sldb/api/stores/merge_driver_install.py) existe, pero solo corre con 'sldb stores merge-driver --install' a mano, y no está instalado en ninguno de los repos con store (sldb, deskops, IR). Sin el driver, un cherry-pick o un rebase que choca en .sldb/ deja marcadores de conflicto que no se pueden resolver por CLI, y el coordinador terminó resolviéndolos a mano (prohibido).

## Goal

_Describe the concrete result this task must produce._

(1) init_store y scaffold_store (sldb stores init/scaffold) y build_store (sldb stores build) llaman a install_merge_driver cuando el store está dentro de un repo git. Es idempotente; fuera de git no hacen nada, y si git falla avisan sin romper el comando. (2) sldb stores check informa un hallazgo 'merge-driver-missing' (nivel warning, con fix: 'sldb stores merge-driver --install') cuando el store está en un repo git y faltan las líneas de .gitattributes o las claves merge.sldb.* de la config.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/stores/init_store.py, scaffold_store.py, build_store.py, store_check.py (o el módulo de hallazgos que use), y tests en tests/api/ o tests/store/; CHANGELOG. Fuera: deskops (tiene su propia nota) y cambiar el driver mismo.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests que fallen antes, en un repo git temporal: (a) stores init deja .gitattributes con las tres líneas y merge.sldb.driver en la config; (b) stores build en un repo sin driver lo instala; (c) correr dos veces no duplica líneas; (d) un store fuera de git: init y build funcionan y no escriben .gitattributes; (e) stores check en un repo sin driver da el hallazgo merge-driver-missing con el fix, y después de instalarlo ya no lo da. p2: implementar reusando install_merge_driver. p3: CHANGELOG; quick_gates (bash tools/check.sh --fast) en 0 y commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan; la suite completa la corre integrate y el integrador corre también la de deskops.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
