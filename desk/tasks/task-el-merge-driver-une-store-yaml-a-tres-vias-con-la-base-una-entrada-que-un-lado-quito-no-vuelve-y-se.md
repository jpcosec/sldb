---
sldb:
  by: agent
  at: '2026-11-23T01:34:45Z'
  authority: generated
  via: save_document_payload
id: task-el-merge-driver-une-store-yaml-a-tres-vias-con-la-base-una-entrada-que-un-lado-quito-no-vuelve-y-se
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-194256-suggestion-ci-de-main-en-rojo-workbench-demo-sin-clasificar-y-un-test-de-ts.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El merge driver une store.yaml a tres vías con la base: una entrada que un lado quitó no vuelve, y se quita del store.yaml la ruta resucitada que rompe el job store de CI

## Rationale

_Explain why this task exists or the business driver behind it._

Encontrado al triar la nota desk/inbox/20261120-194256 (CI de main en rojo). En la última ejecución de CI de main (run 45031355948, 2026-11-22) el job store falla. 'sldb stores build --check' dice 'FAIL: the sources do not rebuild the store' y 'declared, no file: desk/tasks/task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding.md'. El closeout 651a42a0 quitó esa ruta de .sldb/store.yaml, pero el merge e7e348f1 ('merge origin/main ... antes de integrar notations validate') la volvió a agregar. merge_driver() (src/sldb/api/stores/merge_driver.py) recibe la base %O y no la usa, y merge_declaration_data/merge_includes (src/sldb/api/stores/store_file_merge.py) unen ours y theirs. Así, una ruta que una rama retiró y la otra todavía tiene resucita en cada merge. Sigue en origin/main 6ab01b80 (.sldb/store.yaml línea 3052). La parte de workbench_demo de la misma nota es una decisión de JP: task-clasificar-workbench-demo-en-contracts-identity-toml-producto-autoaplicacion-o-ajeno-la-puerta-ident.

## Goal

_Describe the concrete result this task must produce._

merge_driver une store.yaml a tres vías. Una ruta, un link, un modelo o un predicado que está en la base y que un lado quitó no aparece en el resultado. Lo que agregó cualquiera de los dos lados sí aparece. Además, .sldb/store.yaml ya no declara el .md retirado de notations validate, y 'sldb stores build --check' no reporta 'declared, no file'.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/stores/merge_driver.py (leer la base) y src/sldb/api/stores/store_file_merge.py (merge_declaration_data y merge_includes con base). Tests en tests/store/test_merge_driver_auto_install.py o un archivo hermano en tests/store/: base con la ruta X, ours sin X, theirs con X; el resultado no tiene X. Y un caso simétrico que agrega. Regenerar .sldb/store.yaml con 'sldb stores declare --write' en el worktree que dispatch le da al ejecutor, sin editarlo a mano. CHANGELOG.md. Fuera: los índices derivados (store_index.yaml, models/*.yaml), que ya repara rebuild-index, y la clasificación de workbench_demo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test que falla con la unión de hoy. 2) Unión a tres vías en store_file_merge.py, con la base pasada desde merge_driver(); si la base falta o no se puede leer, unión como hoy. 3) sldb stores declare --write y verificar que la línea del .md retirado desapareció. 4) sldb stores build --check. 5) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
- sldb stores build --check
- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos del driver pasan; 'grep -c task-sldb-notations-validate-valida .sldb/store.yaml' no encuentra la ruta bajo desk/tasks/; 'sldb stores build --check' no reporta 'declared, no file'; la suite completa sale rc 0.
