Task: task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras
Title: docs/architecture/command-taxonomy.md lista cada operación de sldb una sola vez, con las cuatro caras que la exponen hoy
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:02:57Z'
  authority: generated
  via: save_document_payload
id: task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras
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

# docs/architecture/command-taxonomy.md lista cada operación de sldb una sola vez, con las cuatro caras que la exponen hoy

## Rationale

_Explain why this task exists or the business driver behind it._

ADR docs/architecture/one-command-taxonomy-served-by-fastmcp.md (JP, 2026-11-25): sldb creció sin una taxonomía de comandos. sldb.api tiene 192 nombres públicos, la CLI unos 20 grupos, sldb serve unas 30 rutas y sldb mcp 15 herramientas; los nombres no coinciden y cada cara cubre un subconjunto distinto. La taxonomía es el paso 1 del ADR y de ella dependen el servidor fastmcp y el compositor de interfaces.

## Goal

_Describe the concrete result this task must produce._

Una tabla de operaciones que JP pueda aprobar: cada operación con sustantivo, verbo, si lee o escribe, nivel de permiso, y el nombre con que aparece hoy en sldb.api, en la CLI, en sldb serve y en sldb mcp; con duplicados, huecos y renombres marcados y un nombre canónico propuesto.

## Scope

_State what is in scope and what is out of scope._

Dentro: el documento docs/architecture/command-taxonomy.md y una prueba que lo mantiene completo. Fuera: renombrar o mover código, el servidor fastmcp, tocar la CLI. Es un inventario; no cambia comportamiento.

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de crear nada, revisar si SurfaceDoc (knowledge/surfaces/) y sldb selfdoc ya guardan y chequean parte de esto, y decir en el documento qué se reutiliza. Leer el ADR y docs/architecture/mcp.md. Los nombres se sacan del código (sldb.api.__all__, el parser de la CLI, el enrutador de src/sldb/cli/serve, el registro de src/sldb/mcp), no a mano.

Aclaraciones de la revisión: público = sldb.api.__all__; comando hoja = subcomando de argparse sin subcomandos propios (sin alias ni ocultos aparte; los ocultos van en la lista final); rutas = cada (método, path) de sldb serve, sin /docs, /openapi.json ni estáticos. Nivel de permiso con tres valores: lee, escribe-store, efecto-externo (git, red, procesos); una operación que lee y escribe es escribe-store. Nombre canónico en snake_case sustantivo_verbo (p. ej. documents_create); en empate, el nombre de sldb.api. Sin operación = nombre que es alias, ayuda o utilidad interna, con su motivo en una línea. SurfaceDoc/selfdoc: se citan como fuente cuando ya registran la operación; no se modifican. La aprobación de JP es posterior y fuera de esta tarea.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_command_taxonomy.py

## Done When

_Name the observable condition that makes the task complete._

Cada nombre público de sldb.api, cada comando hoja de la CLI, cada ruta de sldb serve y cada herramienta de sldb mcp aparece en exactamente una fila, o en una lista final "sin operación" con su motivo. Cada fila dice si lee o escribe. Las filas con más de un nombre para lo mismo y las operaciones que faltan en alguna cara están marcadas. La prueba falla si se agrega una ruta, una herramienta, un comando o un nombre público que no esté en el documento.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-2bcf3e00598e"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-2bcf3e00598e`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-2bcf3e00598e

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
