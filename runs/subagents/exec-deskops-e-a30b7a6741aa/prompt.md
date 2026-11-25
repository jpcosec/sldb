Task: task-surface-dev-astryx-probe-muestra-un-nodo-de-react-flow-y-un-editor-codemirror-como-componentes-de-un
Title: surface/dev/astryx-probe muestra un nodo de React Flow y un editor CodeMirror como componentes de un paquete de integración de Astryx, en la plantilla ide sobre React 19
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
  at: '2026-11-25T18:01:29Z'
  authority: generated
  via: save_document_payload
id: task-surface-dev-astryx-probe-muestra-un-nodo-de-react-flow-y-un-editor-codemirror-como-componentes-de-un
status: active
summary: ''
tags: []
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

# surface/dev/astryx-probe muestra un nodo de React Flow y un editor CodeMirror como componentes de un paquete de integración de Astryx, en la plantilla ide sobre React 19

## Rationale

_Explain why this task exists or the business driver behind it._

ADR docs/architecture/surface-is-an-editor-contract.md (JP, 2026-11-25): surface pasa a ser un contrato de editores sobre Astryx, con el editor de texto (CodeMirror) y el de grafo (React Flow) como componentes paralelos a los de Astryx. La sección "Not verified" del ADR deja cuatro cosas sin comprobar; de ellas dependen el contrato y la reescritura de las tareas del panel embebible de graph_ui.

## Goal

_Describe the concrete result this task must produce._

Una prueba mínima que responda con hechos lo no verificado del ADR: qué exige un paquete de integración de Astryx, si los estilos de React Flow conviven con los de Astryx, cuánto cuesta el build, y si una máquina de XState se prueba sin navegador en ese armado.

## Scope

_State what is in scope and what is out of scope._

Dentro: una carpeta nueva surface/dev/astryx-probe/ con su propio package.json. Fuera: migrar surface/src a React 19, tocar graph_ui, decidir el contrato. No se modifica la app existente.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer la documentación de integraciones con el CLI (npx @astryxdesign/cli docs cli/commands/integration) antes de escribir. Armar el paquete con integration add component para dos componentes: uno que envuelve un lienzo de @xyflow/react con un nodo, otro que envuelve un editor de CodeMirror 6 con una decoración de rango. Montarlos en una página generada con la plantilla ide. Una máquina de XState de tres estados (editando, validando, guardado) con su prueba en vitest.

## Validation

_List the checks required before this task can close._

- cd surface/dev/astryx-probe && npm test
- cd surface/dev/astryx-probe && npx @astryxdesign/cli integration check
- cd surface/dev/astryx-probe && npm run build

## Done When

_Name the observable condition that makes the task complete._

npx @astryxdesign/cli integration check pasa en el paquete. La página construida muestra los dos componentes y cambia entre un tema claro y uno oscuro de Astryx sin que el lienzo ni el editor queden con colores propios. La prueba de la máquina corre sin navegador. surface/dev/astryx-probe/RESULTADO.md responde, con lo observado, las cuatro preguntas del objetivo y dice qué habría que cambiar en el ADR.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-surface-dev-astryx-probe-muestra-un-nodo-de-react-flow-y-un-editor-codemirror-como-componentes-de-un"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-a30b7a6741aa"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-a30b7a6741aa`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-a30b7a6741aa

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
