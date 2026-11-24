Task: task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb
Title: Plan del drawer: motor Datalog duenio de las aristas (revierte D5) y daemon residente de sldb, con prueba de concepto medida y decisiones para JP
Status: active
Current node: ritual-testing
Task type: task.docs
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-24T02:45:50Z'
  authority: generated
  via: save_document_payload
id: task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261123-142527-suggestion-decisi-n-de-jp-el-grafo-de-sldb-pasa-a-un-motor-datalog-revierte-d5.md
- desk/inbox/20261123-142553-suggestion-jp-pide-ver-ahora-el-daemon-de-sldb.md
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Plan del drawer: motor Datalog duenio de las aristas (revierte D5) y daemon residente de sldb, con prueba de concepto medida y decisiones para JP

## Rationale

_Explain why this task exists or the business driver behind it._

Notas 20261123-142527-suggestion-decisi-n-de-jp-el-grafo-de-sldb-pasa-a-un-motor-datalog-revierte-d5 y 20261123-142553-suggestion-jp-pide-ver-ahora-el-daemon-de-sldb (JP 2026-11-23): JP revierte D5 de desk/drawer/plans/grafo-operable/decisiones.md y pide que el grafo pase a un motor Datalog estable que sea duenio del almacenamiento y la consulta de aristas (hoy GraphBackend en src/sldb/store/graph/backend/protocol.py solo cubre eval/analyze sobre networkx; componer el indice, federar stores y live stale van a mano sobre YAML en .sldb_cache/edges: 28 s la primera carga del indice federado, specir catalog build no termina en 280 s). Tambien pide ver ahora el daemon de sldb (diferido desde 2026-11-15): un proceso residente con el indice de aristas y el store cargados para que el CLI, sldb serve, deskops y specir no recompongan el indice en cada invocacion.

## Goal

_Describe the concrete result this task must produce._

Existe desk/drawer/plans/grafo-datalog-daemon/ con alcance, brief, decisiones y dag.yaml que cubre las dos cosas juntas; decisiones.md de grafo-operable registra D5 revertida por JP el 2026-11-23; el plan trae los resultados de una prueba de concepto que carga el indice federado real en un motor Datalog embebido (Datalevin u otro con cliente Python) y mide aristas de un nodo, recorrido, emparejamiento de atomos y stale contra el camino actual; y cada decision de diseno abierta queda como una task.decision para JP.

## Scope

_State what is in scope and what is out of scope._

Entra: comparar motores Datalog con cliente Python (Datalevin como candidato de docs/architecture/graph-backend.md) y elegir uno para la prueba; prueba de concepto fuera del codigo de produccion (scripts en reports/ o en el plan) con mediciones; para el daemon: que queda residente, como lo encuentra el CLI, que pasa sin daemon en contenedores de ejecutor y en tests, como se invalida con git, relacion con sldb serve y con los hooks actuales, consumo de memoria en robocop2 con el tope de 8 GB libres; task.decision por cada decision (motor, forma del daemon, invalidacion). Fuera: cambiar GraphBackend o el codigo de produccion; eso sale de tareas que el plan propone. No reemplaza ni bloquea task-matching-attach-atom-edges-deja-de-recomponer-live-stale..., que va primero.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/graph-backend.md, desk/drawer/plans/grafo-operable/ y el codigo de GraphBackend, compose y edge_index. 2) Prueba de concepto: exportar el indice federado real a hechos y cargarlo en el motor; medir las cuatro consultas contra el camino actual, con RSS. 3) Escribir el plan (alcance, brief, decisiones, dag.yaml) con el daemon. 4) Registrar D5 revertida en grafo-operable/decisiones.md. 5) Crear las task.decision con deskops add task --task-type task.decision.

## Validation

_List the checks required before this task can close._

- deskops graph missing --root . sin faltantes nuevos; la prueba de concepto se puede repetir con el comando que deja el informe

## Done When

_Name the observable condition that makes the task complete._

El plan existe con dag.yaml valido (deskops review node puede leerlo); el informe trae la tabla de tiempos y memoria de la prueba de concepto contra el camino actual; D5 aparece como revertida con fecha y motivo; hay una task.decision por decision abierta, con opciones y recomendacion.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-26633313df8f-a2"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-26633313df8f-a2`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-26633313df8f-a2

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
