Task: task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer
Title: sldb move mueve un archivo o directorio con git mv y actualiza en el mismo repo el store y las referencias a la ruta vieja
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-19T18:44:40Z'
  authority: generated
  via: create_document
id: task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb move mueve un archivo o directorio con git mv y actualiza en el mismo repo el store y las referencias a la ruta vieja

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP, 2026-11-19. Hoy mover un archivo del repo deja todo roto: move_document (src/sldb/api/documents/move_document.py) existe solo en la API y en Transaction, mueve con Path.rename (git lo ve como borrado más alta, no como renombre), no tiene CLI, y solo re-trackea el documento movido. Los campos de otros documentos que nombran la ruta vieja quedan apuntando a la nada: target_identity de las materializations, files y references de las tareas, provenance de los atoms. Lo mismo pasa con los links Markdown a esa ruta. Hoy eso se arregla a mano, y está prohibido tocar el store a mano.

## Goal

_Describe the concrete result this task must produce._

sldb move <origen> <destino> [--store S] [--dry-run] [--format text|json] mueve un archivo o un directorio dentro del proyecto. (1) Si el origen está versionado en git, usa git mv, así git registra el renombre; si no, mueve en disco. (2) Los documentos trackeados que se mueven siguen trackeados con el mismo nombre, como hace move_document. (3) En los documentos trackeados del store del proyecto, todo valor de campo que sea exactamente la ruta vieja, o que empiece por la ruta vieja más '/' cuando el origen es un directorio, pasa a la ruta nueva, escrito por la API de campos de sldb y no como texto. (4) En los archivos Markdown del repo, los links relativos e inline a la ruta vieja apuntan a la nueva. (5) Todo pasa en una Transaction: si algo falla, el árbol y el store quedan como estaban. (6) --dry-run lista lo que movería y cada referencia que reescribiría (documento, campo y valor viejo y nuevo, o archivo y línea) sin tocar nada. La salida json da esa misma lista.

## Scope

_State what is in scope and what is out of scope._

Dentro: el comando CLI (parser y comando en src/sldb/cli/), una función de API move_path (en src/sldb/api/documents/, exportada en sldb.api) que reusa move_document para cada documento trackeado bajo el origen, el reescritor de referencias de campos y de links Markdown, tests en tests/api/ y tests/cli/, la referencia de CLI regenerada con selfdoc sync, docs y CHANGELOG. Fuera: reescribir referencias en otros repos o stores enlazados (solo el propio repo), ediciones de texto libre que no sean el valor completo de un campo o el destino de un link Markdown, y cambiar move_document salvo para usar git mv.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: leer move_document.py, transaction.py y transaction_ops.py (el paso move), y cómo se escriben campos (save_document_payload, fields update). p2: tests que fallen antes, en un repo git temporal con un store: (a) mover un documento trackeado: git status muestra un renombre (R), el documento sigue trackeado con el mismo nombre y stores check queda en 0; (b) mover un archivo de código que un campo de otro documento nombra (p. ej. una materialization con target_identity igual a esa ruta): el campo queda con la ruta nueva; (c) mover un directorio: los campos con la ruta vieja como prefijo se actualizan, y un hermano con prefijo parecido (dir vs dirzero) no se toca; (d) un link Markdown relativo a la ruta vieja apunta a la nueva; (e) --dry-run no cambia nada y lista lo mismo que haría; (f) destino existente o fuera del proyecto: error y nada cambia; (g) un fallo a mitad restaura todo. p3: implementar. p4: como es un comando nuevo, 'PYTHONPATH=src sldb selfdoc sync' y commitear la referencia; 'selfdoc check' en 0. p5: docs y CHANGELOG. p6: quick_gates (bash tools/check.sh --fast) en 0, y commit con rutas nombradas y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py tests/cli/test_move_cli.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan, selfdoc check y tools/check.sh --fast dan 0, y la suite completa la corre integrate. El integrador corre además la suite de deskops contra este sldb antes de integrar.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.
