FILE:desk/tasks/task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam.md
---
sldb:
  by: agent
  at: '2026-11-16T04:12:29Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md
depends_on: []
pills: []
files:
- docs/versionado-y-colaboracion.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
---

# Decisión de JP: cómo se resuelve un conflicto de git en los índices derivados de .sldb (store_index.yaml y models/*.yaml)

## Rationale

_Explain why this task exists or the business driver behind it._

.sldb/core/store_index.yaml (store_hash) y .sldb/core/models/<Modelo>.yaml (roster_hash, documents_count) son los niveles del Merkle derivados de los shards de documents/ (documents_hash._hash_b, hashing.hash_model_layer, ops.cascade_store_hash). Cualquier escritura reescribe esas líneas, así que dos ramas que tocan documentos distintos siempre chocan en store_hash aunque los shards se mezclen limpios. sldb stores update arranca con load_store_index (src/sldb/store/io/__init__.py:79), que falla con marcadores de conflicto; en a3514755 se quitaron a mano. No hay .gitattributes ni merge driver. Hueco 2 de la nota: stores build sin store.yaml. Pasa en cada rebase de mepu y en cada integración de SLDB_1. Cambia qué se versiona en git, por eso es del dueño. Origen: desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md.

## Goal

_Describe the concrete result this task must produce._

JP elige una opción y queda escrita en docs/versionado-y-colaboracion.md, sección "Conflictos en los índices derivados", con la fecha; se crea con deskops add task la tarea de código que la implementa.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones con su costo: (a) sldb stores update reconstruye store_index.yaml y models/*.yaml desde los shards cuando no se pueden leer (marcadores de conflicto): un comando resuelve el conflicto, git sigue versionando los derivados; (b) un merge driver de git declarado en .gitattributes que regenera esos archivos durante el merge (automático pero requiere configurar git en cada clon); (c) dejar de versionar los derivados y regenerarlos al leer (sin conflictos; cambia la regla de que .sldb/core va en git, ver el atom atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past). Recomendación del coordinador: (a), por ser local a sldb y reversible. Registrar el recibo owner (dispose accepted de JP), escribir la sección y crear la tarea de código con tests en tests/store/test_update_fault_tolerance.py y tests/store/test_merkle_shards.py. No entra: implementar; el hueco 2 (stores build sin store.yaml) entra en la tarea de código si JP elige (a) o (b).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la nota, docs/versionado-y-colaboracion.md y el atom citado. 2) Pedir la decisión a JP. 3) Escribir la sección. 4) Crear la tarea de código con deskops add task y references a esta nota.

## Validation

_List the checks required before this task can close._

- grep -n 'Conflictos en los índices derivados' docs/versionado-y-colaboracion.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; la tarea de código existe en desk/tasks; commit del doc.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

