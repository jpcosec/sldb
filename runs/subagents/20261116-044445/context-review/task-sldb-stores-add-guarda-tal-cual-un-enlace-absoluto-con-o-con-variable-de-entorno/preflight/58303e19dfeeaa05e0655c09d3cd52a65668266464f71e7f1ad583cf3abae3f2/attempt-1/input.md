FILE:desk/tasks/task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno.md
---
sldb:
  by: agent
  at: '2026-11-16T04:10:12Z'
  authority: generated
  via: create_document
id: task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-sldb-stores-add-guarda-siempre-el-enlace-relativo-no-resuelve-desde-worktrees-un-nivel-más-hondo.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/link_store.py
- src/sldb/store/query.py
- tests/api/test_api_stores.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
---

# sldb stores add guarda tal cual un enlace absoluto, con ~ o con variable de entorno

## Rationale

_Explain why this task exists or the business driver behind it._

record_store_link (src/sldb/api/stores/link_store.py:71) guarda siempre rel = os.path.relpath(other, root) (línea 89), aunque se le pase una ruta absoluta. Con clones en /srv/repos/<repo> y worktrees en /srv/wt/<repo>/<rama>, un nivel más hondo, el mismo enlace versionado no resuelve en los dos (AntonIA: shared_llm-gateway 479b415 y manifest 9729506 quedaron con '../../../mnt/ssd/proyectos/SLDB_1/deskops-runtime/.sldb'). La lectura ya acepta entradas absolutas (_linked_stores en src/sldb/store/query.py:108-114 vía _resolve_path). Origen: desk/inbox/inbox-note-sldb-stores-add-guarda-siempre-el-enlace-relativo-no-resuelve-desde-worktrees-un-nivel-más-hondo.md.

## Goal

_Describe the concrete result this task must produce._

`sldb stores add <ruta>` guarda la ruta como la escribió el usuario si empieza por /, ~ o $ (absoluta, home o variable de entorno) y relativa a la raíz del proyecto en cualquier otro caso (como hoy); la lectura expande ~ y variables de entorno al resolver el enlace.

## Scope

_State what is in scope and what is out of scope._

Entra: en record_store_link decidir la forma guardada según el texto original (no según la ruta resuelta), lo que exige pasar el texto original desde el comando (src/sldb/cli/commands/ del verbo stores add) hasta la API; en _resolve_path / _linked_stores (src/sldb/store/query.py) aplicar os.path.expandvars y os.path.expanduser antes de resolver; stores remove y stores add --replace siguen funcionando con cualquiera de las tres formas. Tests en tests/api/test_api_stores.py: ruta absoluta guardada absoluta; ~/x guardada como ~/x y resuelta con HOME parcheado; $SLDB_TEST_ROOT/x guardada tal cual y resuelta con la variable puesta; ruta relativa guardada relativa como hoy. tests/api/test_unlink_store.py sigue verde. CHANGELOG.md y la sección de enlaces en docs/ (grep "stores add" docs/). No entra: resolver contra el git common dir (la otra opción de la nota), migrar enlaces ya guardados.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/stores/link_store.py (record_store_link y su llamador), el comando stores add en src/sldb/cli/commands/ (grep -rn "record_store_link\|link_store" src/sldb/cli), y src/sldb/store/query.py 100-120. 2) Pasar el texto original. 3) Guardar según prefijo. 4) Expandir al leer. 5) Tests, doc y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm pytest -q tests/api/test_unlink_store.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los cuatro casos nuevos; CHANGELOG y doc; commit; aviso a AntonIA con deskops message send --to AntonIA (si ese repo no está registrado para el envío, el aviso va como línea "Aviso a AntonIA" en el informe de cierre).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

