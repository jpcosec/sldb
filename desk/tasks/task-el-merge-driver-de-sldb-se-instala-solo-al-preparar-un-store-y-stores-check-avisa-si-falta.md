---
sldb:
  by: agent
  at: '2026-11-20T07:42:11Z'
  authority: generated
  via: save_document_payload
id: task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Regresión en el consumidor, detectada por el coordinador
  al correr la suite de deskops contra 68d4ee1d: tests/test_transaction.py::test_split_restores_source_and_store_when_the_second_atom_create_fails
  de deskops falla 3 de 3 con este commit y pasa 3 de 3 sin él (sldb fd3c024b). Causa:
  el split de deskops hace un build del store dentro de una Transaction; ensure_merge_driver,
  llamado desde build_store/init_store/scaffold_store de la API, escribe .gitattributes
  y la config de git fuera del snapshot de la transacción, y el rollback no lo deshace.
  Después del split fallido, ''stores check'' ya no da lo mismo que antes, porque
  cambia la lista de alerts. Intento 2: la instalación automática va solo en los comandos
  CLI (''sldb stores init'', ''sldb stores scaffold'', ''sldb stores build'', en src/sldb/cli/commands/),
  no en las funciones de API que usan las transacciones y deskops. El hallazgo merge-driver-missing
  de stores check se queda, porque solo lee. Test: un build o init por la API dentro
  de una Transaction que falla no deja .gitattributes ni merge.sldb.* nuevos; los
  tests actuales del CLI siguen pasando. Antes de entregar, correr también ese test
  de deskops con PYTHONPATH a este sldb si el contenedor tiene deskops (/workspace/deskops).'
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
