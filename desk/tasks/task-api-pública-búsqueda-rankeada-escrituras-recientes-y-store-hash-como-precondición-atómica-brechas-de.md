---
sldb:
  by: agent
  at: '2026-11-15T15:52:12Z'
  authority: generated
  via: create_document
id: task-api-pública-búsqueda-rankeada-escrituras-recientes-y-store-hash-como-precondición-atómica-brechas-de
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# API pública: búsqueda rankeada, escrituras recientes y store_hash como precondición atómica (brechas de IR01, inbox 20261114-074447)

## Rationale

_Explain why this task exists or the business driver behind it._

La auditoría IR01 de specIR halló tres brechas en la API pública que el MCP necesita.

## Goal

_Describe the concrete result this task must produce._

Resolver o documentar con decisión cada brecha.

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261114-074447, tres capacidades: (4) search no puntúa ni ordena por relevancia, exponer puntaje y orden; (9) journal devuelve siempre vacío, exponer la consulta de escrituras recientes con fecha y procedencia, que se cruza con el pedido de escucha y eventos del inbox 20261114-115028; (10) aceptar StoreFingerprint.store_hash como precondición de una escritura y rechazar el mismatch de forma atómica, que se apoya en las guardas bajo el cerrojo (inbox 20261115-022444). Antes de implementar cada una, verificar contra HEAD y decidir si se hace aquí o se pliega en otra tarea; la capacidad de deshacer de esa nota ya es su propia tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Cada capacidad con test y documentación, o con decisión registrada de no hacerla; suite de a un archivo, tools/check.sh y stores build --check.
