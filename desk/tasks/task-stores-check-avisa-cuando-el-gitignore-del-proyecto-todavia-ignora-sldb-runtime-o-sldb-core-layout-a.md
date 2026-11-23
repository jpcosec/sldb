---
sldb:
  by: agent
  at: '2026-11-23T01:32:19Z'
  authority: generated
  via: save_document_payload
id: task-stores-check-avisa-cuando-el-gitignore-del-proyecto-todavia-ignora-sldb-runtime-o-sldb-core-layout-a
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261119-220305-unclear-revisar-las-l-neas-de-gitignore-que-pone-init.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# stores check avisa cuando el .gitignore del proyecto todavía ignora .sldb/runtime/ o .sldb/core/ (layout anterior a c420809c) y nombra stores migrate-layout como arreglo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261119-220305 (hbc_latina, 2026-11-19), punto 2: los repos inicializados antes de c420809c (2026-11-04) siguen con .sldb/runtime/ en su .gitignore, por ejemplo heyantonia/plantilla_cliente, que además lo hereda a los repos que genera, y nada avisa hasta que alguien corre stores migrate-layout. En origin/main 6ab01b80, _OLD_SPLIT de src/sldb/api/stores/gitignore_lines.py solo lo usa rewrite_for_split, que se llama desde migrate_layout.py; ni init_store.py (ensure_cache_ignored) ni stores check miran esas líneas. Punto 1 (.deskops.log sin ignorar): el archivo lo escribe deskops y la nota tiene su gemela en el inbox de deskops (20261119-220154). Por eso las líneas de .gitignore de deskops son de deskops y quedan fuera; sldb solo es dueño de .sldb_cache/ y del layout viejo.

## Goal

_Describe the concrete result this task must produce._

sldb stores check emite una alerta 'gitignore-old-layout' cuando el .gitignore de la raíz del proyecto tiene una línea que ignora .sldb/core o .sldb/runtime. La alerta nombra la línea y da como fix 'sldb stores migrate-layout'. Un .gitignore sin esas líneas no da alerta.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/stores/gitignore_lines.py (una función que devuelve las líneas viejas, reutilizando _OLD_SPLIT y pattern_of); el armado de alertas de stores check, siguiendo el patrón de src/sldb/api/stores/ensure_merge_driver.py con su alerta 'merge-driver-missing'; tests en tests/api/test_gitignore_policy.py; CHANGELOG.md. Fuera: .deskops.log y cualquier línea de deskops. Tampoco se reescribe el .gitignore solo, porque eso ya lo hace migrate-layout.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) old_layout_lines(gitignore) en gitignore_lines.py. 2) Alerta en stores check con el mismo helper alert() que usa ensure_merge_driver.py. 3) Dos tests en tests/api/test_gitignore_policy.py: un .gitignore con '.sldb/runtime/' da la alerta con el fix; uno con solo '.sldb_cache/' no la da. 4) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q -p no:cacheprovider tests/api/test_gitignore_policy.py
- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan, stores check sobre un proyecto con '.sldb/runtime/' en .gitignore muestra la alerta con 'sldb stores migrate-layout', y la suite completa sale rc 0.
