Task: task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg
Title: matching: attach_atom_edges deja de recomponer live-stale y los mapas del índice federado en cada edges_of (catalog build con átomos en minutos)
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.debug
Effective pills:
- desk/contexts/pill-pill-una-carga-del-índice-en-attach-atom-edges.md
Effective atoms:
- atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-debug] TaskDebugDoc:task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg: Una tarea task.debug se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg-bundle-1 {"kind":"bundle"})

---
sldb:
  by: agent
  at: '2026-11-23T18:03:26Z'
  authority: generated
  via: save_document_payload
id: task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md
depends_on: []
pills:
- desk/contexts/pill-pill-una-carga-del-índice-en-attach-atom-edges.md
files:
- src/sldb/api/matching/store_reader.py
- src/sldb/api/matching/store_edges.py
- src/sldb/store/edge_index/composed_reading.py
- tests/matching/test_matching_refs.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
---

# matching: attach_atom_edges deja de recomponer live-stale y los mapas del índice federado en cada edges_of (catalog build con átomos en minutos)

## Rationale

_Explain why this task exists or the business driver behind it._

IR13 midió que `specir catalog build --config <project.yml de ejemplo del catálogo en las fixtures visuales del repo IR>` (repo IR) no termina en 300 s; el tiempo es de sldb. cProfile: 146 de 149 s en sldb.api.matching.attach_atom_edges -> StoreReader.edges_of (31 llamadas) -> store_edges.edges_of -> edges_from + edges_to -> load_edge_index (62 llamadas, ~1,1 s cada una). compose_edge_index acierta la caché _COMPOSED, pero with_live_stale corre stale_of_facts en cada llamada y el model_copy resultante reconstruye los mapas (_ensure_maps). Origen: desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md.

## Goal

_Describe the concrete result this task must produce._

attach_atom_edges sobre N referencias llama a load_edge_index a lo sumo 2 veces por llamada (una con enlaces y otra sin ellos, si hacen falta las dos) y no recalcula live-stale ni los mapas por cada referencia; el catalog build de IR de la nota termina en menos de 60 s con el mismo resultado.

## Scope

_State what is in scope and what is out of scope._

Entra, en este orden: (1) reproducir con un test de rendimiento acotado en tests/matching/ que cuenta llamadas (monkeypatch de load_edge_index o de stale_of_facts con un contador) para 10 referencias sobre un store de prueba y falla si load_edge_index se llama más de 2 veces; (2) arreglar en src/sldb/api/matching/store_reader.py (StoreReader, líneas 45-57) para que cargue el índice una vez por store y resuelva edges_from y edges_to de cada referencia sobre ese índice ya cargado, en lugar de llamar store_edges.edges_of por referencia; (3) solo si (2) no basta para la meta, memoizar with_live_stale en src/sldb/store/edge_index/composed_reading.py (líneas 43-47) por firma de shards y stats de fuentes. Medición antes y después con el comando de IR de la nota (cd al repo IR, timeout 300) y guardada en el informe del ejecutor. CHANGELOG.md. No entra: cambiar la semántica de stale (sigue reportando las ediciones externas), tocar compose.py salvo que (3) lo exija, ni la configuración de federación del store de IR (la doble federación deskops/sldb de SLDB_1 y ~/herramientas es configuración de IR, no código de sldb).

Precisiones (preflight-1): la meta es una carga por store y por llamada a attach_atom_edges; el test admite 2 porque edges_from y edges_to pueden necesitar el índice con y sin enlaces. Si se llega al paso (3), la clave de la memoización es (store_path, shards_signature(store_path), tupla ordenada de (ruta, mtime_ns, tamaño) de los archivos trackeados) y la caché vive en el proceso. "Mismo resultado" es igualdad de las aristas devueltas por attach_atom_edges antes y después, comparadas como conjuntos en el test. El comando de la nota es `cd /mnt/ssd/proyectos/SLDB_1/IR && timeout 300 specir catalog build --config <ruta del project.yml de ejemplo que cita la nota>`; la ruta exacta se copia de la nota de origen (references). El store de prueba del test contador se arma como en tests/matching/test_matching_refs.py.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/matching/store_reader.py, src/sldb/api/matching/store_edges.py (línea 28), src/sldb/api/edges/edge_reading.py (edges_from línea 45, edges_to línea 61), src/sldb/store/edge_index/compose.py (línea 48), composed_reading.py (43-47) y edge_index.py (_ensure_maps, línea 43). 2) Test contador que falla hoy. 3) Cambio en StoreReader. 4) Medir; si no alcanza, memoización del paso (3). 5) Correr los tests de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/store/test_live_stale_security.py

## Done When

_Name the observable condition that makes the task complete._

El test contador pasa (load_edge_index a lo sumo 2 veces para 10 referencias); los tres comandos de Validation pasan; la medición del catalog build de IR antes/después queda en el informe con el después bajo 60 s; commit.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-3617fe0f6a32-a2"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-3617fe0f6a32-a2`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-3617fe0f6a32-a2

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
