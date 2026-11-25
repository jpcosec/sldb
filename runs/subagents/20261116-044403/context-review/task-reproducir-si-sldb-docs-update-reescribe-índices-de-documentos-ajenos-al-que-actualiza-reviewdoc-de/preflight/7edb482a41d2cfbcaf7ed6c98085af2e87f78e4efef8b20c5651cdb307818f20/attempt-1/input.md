FILE:desk/tasks/task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de.md
---
sldb:
  by: agent
  at: '2026-11-16T04:09:47Z'
  authority: generated
  via: create_document
id: task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-sldb-docs-update-valida-y-reescribe-documentos-ajenos-al-que-actualiza.md
depends_on: []
pills: []
files:
- tests/store/test_doc_invalid_writes.py
- src/sldb/api/documents/payload_save.py
- src/sldb/api/documents/payload_save_steps.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
---

# Reproducir si sldb docs update reescribe índices de documentos ajenos al que actualiza (ReviewDoc de un store enlazado con otro contrato)

## Rationale

_Explain why this task exists or the business driver behind it._

En el kit Chatbot_Infra (enlazado a un checkout viejo de deskops cuyo ReviewDoc no conocía kind evidence), `sldb docs update borrado-de-una-persona` falló con 2 validation errors de ReviewDoc sobre recibos que no eran el documento actualizado, y además dejó modificados 5 ReviewDoc .yaml ajenos sin el tag workspace:desk. La parte "una escritura cae por un vecino inválido" se arregló en 9668e881 (tests/store/test_doc_invalid_writes.py, test_a_transactional_write_of_a_valid_document_touches_only_it). No está verificado si update todavía reescribe shards de índice de otros documentos. Reportado por AntonIA el 2026-11-10. Origen: desk/inbox/inbox-note-sldb-docs-update-valida-y-reescribe-documentos-ajenos-al-que-actualiza.md.

## Goal

_Describe the concrete result this task must produce._

Saber, con un test que lo prueba, si `sldb docs update <doc>` sobre un store que enlaza a otro store cuyo modelo rechaza algunos de sus documentos modifica algún archivo fuera del documento actualizado, su shard y los índices derivados del store (store_index.yaml y models/<Modelo>.yaml del modelo del documento).

## Scope

_State what is in scope and what is out of scope._

Entra: (1) test de reproducción en tests/store/test_doc_invalid_writes.py: store A con un modelo y un documento; store B enlazado desde A con un modelo ReviewDoc-like cuyos documentos dejan de validar al cambiar el modelo (un Literal que pierde un valor); snapshot de bytes de todos los archivos de A y B; `docs update` del documento de A; comparar. (2) Si el test muestra archivos ajenos modificados, arreglar en src/sldb/api/documents/payload_save.py (save_document_payload, línea 15) o en el paso de reconstrucción de src/sldb/api/documents/payload_save_steps.py (línea 112) para que solo se escriban el documento, su shard y los índices derivados que dependen de él, y que los documentos inválidos de B se reporten como alerta. (3) Si no se reproduce con caché caliente ni con caché fría (sin .sldb_cache), el test queda como guarda de regresión y el informe lo dice; la tarea cierra igual. CHANGELOG.md solo si hubo arreglo. No entra: cambiar el modelo ReviewDoc de deskops, tocar el kit Chatbot_Infra.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/store/test_doc_invalid_writes.py (fixtures existentes), payload_save.py y payload_save_steps.py. 2) Escribir el test con snapshot de bytes (dict ruta -> sha256 antes y después). 3) Correrlo con y sin .sldb_cache. 4) Arreglo solo si falla. 5) Informe con resultado de ambas corridas.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_writes.py
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py

## Done When

_Name the observable condition that makes the task complete._

El test de reproducción existe y pasa; el informe dice si se reprodujo (con caché caliente y fría) y, si se reprodujo, qué se cambió; commit; respuesta a AntonIA con deskops message send --to AntonIA (si ese repo no está registrado para el envío, el aviso va como línea "Aviso a AntonIA" en el informe de cierre).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

