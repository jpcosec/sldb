FILE:desk/tasks/task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen.md
---
sldb:
  by: agent
  at: '2026-11-20T01:40:46Z'
  authority: generated
  via: create_document
id: task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El .sldb_cache del repo deja a deskops con una vista vieja de los ReviewDoc: recibos aceptados no cuentan para activar una tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Regresión, 2026-11-20 (repro en runs/subagents/20261120-repro-cache-recibos/repro.log). Los recibos preflight-1 y bundle-1 de la tarea de sldb move están aceptados en disco, pero deskops next en el repo dice que no hay preflight aceptado (rule-activation-task-code, seen: {}). Con el mismo HEAD y los mismos cambios sin commitear, en un worktree limpio sin .sldb_cache, la tarea activa. sldb stores build no refresca la caché. Bloquea al ejecutor de sldb move y a cualquier tarea cuyos recibos se acepten después de que la caché se arme. Sospecha: la caché de filas de documentos de d3568eea (store/query_engine/document_rows_disk.py, clave de stats) o la caché compuesta del índice de aristas de H11.

## Goal

_Describe the concrete result this task must produce._

Después de escribir, actualizar o disponer un documento por la API o los CLI (en particular deskops review dispose, que reescribe el ReviewDoc), toda lectura posterior (select_documents, reglas, edges_holding, deskops next) ve el estado nuevo, sin borrar .sldb_cache a mano. Una caché vieja se invalida sola. Además, sldb stores build deja la caché coherente.

## Scope

_State what is in scope and what is out of scope._

Dentro: la caché que dé la vista vieja (document_rows_disk.py y/o la composición del índice de aristas en src/sldb/store/edge_index/), su clave de invalidación, tests en tests/api/ y CHANGELOG. Fuera: deskops (no se toca; si el fallo resulta estar en deskops, el ejecutor lo informa).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducir en un repo temporal: armar la caché con una lectura (select_documents o rules), reescribir un documento in place con la API de escritura (como hace review dispose: cambio de un campo sin agregar ni quitar archivos) y volver a leer; la lectura debe ver el campo nuevo. Si no se reproduce así, probar con el patrón exacto del repro.log (stores enlazados, ReviewDoc con subject a otro modelo, inverso ^subject) e informar cuál falla. p2: test que falla antes con ese caso. p3: arreglar la clave de invalidación (que cuente lo que cambia en una reescritura in place) o invalidar explícitamente en el camino de escritura; sin quitar la caché. p4: que stores build regenere o invalide la caché. p5: CHANGELOG, quick_gates (bash tools/check.sh --fast) en 0 y commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa; con este sldb, deskops next de la tarea de sldb move en el repo real ya no está bloqueado; la suite completa la corre integrate y el integrador corre también la de deskops.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

