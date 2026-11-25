Task: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond
Title: propose_changes rechaza antes de escribir una relación que viola los tipos, la cardinalidad o la condición de su tipo de relación
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
  at: '2026-11-25T23:11:10Z'
  authority: generated
  via: save_document_payload
id: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond
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
pointers: []
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-3581f6784df9"

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
