Task: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond
Title: propose_changes rechaza antes de escribir una relación que viola los tipos, la cardinalidad o la condición de su tipo de relación
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:10:45Z'
  authority: generated
  via: save_document_payload
id: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond
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

# propose_changes rechaza antes de escribir una relación que viola los tipos, la cardinalidad o la condición de su tipo de relación

## Rationale

_Explain why this task exists or the business driver behind it._

ADR docs/architecture/pron-is-archived.md (JP, 2026-11-25): pron se archiva y la edición desde una interfaz escribe por sldb. Hoy sldb detecta una relación inválida después de escribirla (sldb.api check_edges), y su propio MCP lo declara como faltante (src/sldb/mcp/write/pendings.py, "the missing edge validation"). Rechazar antes de escribir era lo único que tenía solo pron y que la edición por gestos de graph_ui necesita.

## Goal

_Describe the concrete result this task must produce._

Que proponer un lote que crea o cambia una relación devuelva el rechazo, con un motivo por cada violación, antes de tocar el store; y que el mismo lote completo se prevalide como unidad.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/mcp/write/ (propose, pendings, findings), src/sldb/mcp/changes/assert_edge.py y sldb.api.apply_batch con dry_run, reusando las comprobaciones de tipos, cardinalidad y condición que ya hace check_edges. Fuera: portar código de pron, el registro persistente y deshacer entre sesiones (tarea aparte), cualquier interfaz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero docs/architecture/rules.md, edges.md y mcp.md, y cómo check_edges decide que una relación es inválida. La validación previa usa esas mismas funciones sobre el estado que resultaría del lote; no se escribe un segundo validador.

Aclaraciones de la revisión: Simular sin escribir: aplicar el lote sobre una copia en memoria de los documentos afectados (en el orden del lote; una relación puede apoyarse en otra del mismo lote) y correr sobre ella las mismas funciones de check_edges; si exigen store escrito, extraer la parte pura y que check_edges la siga usando. Hash = el root hash del store (store_index) antes y después: igual. Rechazo = la estructura de rechazo que propose_changes ya devuelve hoy, una entrada por violación con la relación (origen, tipo, destino) y el código de la violación (tipo, cardinalidad o condición). Si apply_batch ya tiene dry_run, devuelve los mismos rechazos; si no lo tiene, no se crea. 'Igual que antes' = mismo valor de retorno y mismas escrituras; los tests existentes de mcp/write siguen pasando. pendings: quitar la entrada que hoy marca la validación de relaciones como faltante. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_mcp_propose_rejects_invalid_edges.py
- python -m pytest -q tests -k "mcp or apply_batch or check_edges"

## Done When

_Name the observable condition that makes the task complete._

Un lote con una relación entre modelos que su RelationTypeDoc no admite, otro que excede la cardinalidad y otro que incumple la condición devuelven cada uno un rechazo que nombra la relación y la violación, y el hash del store no cambia. Un lote válido se comporta igual que antes. Un lote con una relación válida y otra inválida se rechaza entero. pendings deja de informar la validación de relaciones como faltante. apply_batch con dry_run informa lo mismo.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-2757adcb50b7"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-2757adcb50b7`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-2757adcb50b7

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
