Task: task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e
Title: resolver una vista informa como hueco el documento que ningún glifo casa, en vez de fallar la vista entera
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:17:11Z'
  authority: generated
  via: save_document_payload
id: task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e
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

# resolver una vista informa como hueco el documento que ningún glifo casa, en vez de fallar la vista entera

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de specIR (desk/drawer/plans/pedidos-de-specir-y-graph-ui/). Hoy un documento que ningún GlyphDoc de la notación casa hace fallar todo el resolve_view con ViewError. Así no se puede medir qué parte de un store cubre una notación, que es lo que hace falta para revisar un estándar (UML, BPMN, IFML, ORCA) como notación.

## Goal

_Describe the concrete result this task must produce._

Que la vista se resuelva con los documentos que sí casan y que el resultado liste aparte los que no, con su id y su modelo.

## Scope

_State what is in scope and what is out of scope._

Dentro: sldb.api.notations (resolve_view, evaluate_projection_view y ViewError) y la ruta de sldb serve que los expone. Fuera: cambiar el formato de NotationDoc, graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/notations-and-views.md. Los huecos van en un campo propio del resultado; un llamador que quiera el comportamiento estricto lo pide de forma explícita.

Aclaraciones de la revisión: Campo gaps en el resultado: lista de {id, model}, donde model es el nombre del modelo del documento (p. ej. TaskCodeDoc). Parámetro strict: bool = False en resolve_view y evaluate_projection_view; con strict=True se conserva exactamente el ViewError de hoy (mismo tipo y mensaje); ViewError no cambia. La ruta de evaluación de vistas de sldb serve (la que llama a evaluate_projection_view, ver src/sldb/cli/serve) devuelve gaps y acepta strict como query param. Sin huecos, gaps es []. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_view_reports_unmatched_documents.py
- python -m pytest -q tests -k "notation or view"

## Done When

_Name the observable condition that makes the task complete._

Una vista sobre un store con un documento sin glifo devuelve los demás nodos y aristas y lista ese documento como hueco con id y modelo. En modo estricto sigue fallando con el mismo error que hoy. sldb notations validate no cambia.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-05461eadbe5b"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-05461eadbe5b`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-05461eadbe5b

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
