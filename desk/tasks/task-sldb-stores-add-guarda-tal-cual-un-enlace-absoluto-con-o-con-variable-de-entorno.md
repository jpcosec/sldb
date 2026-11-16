---
sldb:
  by: agent
  at: '2026-11-16T07:48:50Z'
  authority: generated
  via: save_document_payload
id: task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-sldb-stores-add-guarda-siempre-el-enlace-relativo-no-resuelve-desde-worktrees-un-nivel-más-hondo.md
depends_on: []
pills:
- desk/contexts/pill-pill-validar-el-enlace-guardando-el-texto-tal-cual.md
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

Precisiones (preflight-1): reglas de prefijo sobre el texto tal como lo escribió el usuario: empieza por "/" (absoluta), por "~" (incluido ~user) o por "$" (forma $VAR o ${VAR}) -> se guarda tal cual; cualquier otro texto -> relativo a la raíz como hoy. Un "$" literal en un nombre de carpeta no se soporta (queda como variable). El punto de paso del texto original es el comando de stores add en src/sldb/cli/commands/ (localizarlo con el grep de implementation_path) y la función de API a la que llama; se agrega un parámetro keyword-only raw: str | None = None. La doc a actualizar es docs/architecture/store-declaration.md (sección de enlaces o links).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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
