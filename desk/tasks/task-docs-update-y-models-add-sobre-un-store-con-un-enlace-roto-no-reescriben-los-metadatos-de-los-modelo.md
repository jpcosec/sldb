---
sldb:
  by: agent
  at: '2026-11-23T01:38:11Z'
  authority: generated
  via: save_document_payload
id: task-docs-update-y-models-add-sobre-un-store-con-un-enlace-roto-no-reescriben-los-metadatos-de-los-modelo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-185348-unclear-docs-update-y-models-add-con-un-store-enlazado-roto-reescriben-lo-de-deskops.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs update y models add sobre un store con un enlace roto no reescriben los metadatos de los modelos del store enlazado

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261122-185348 (pedido de Chatbot_Infra del 2026-11-04, reenviado en 6ab01b80). En Chatbot_Infra el store enlazado deskops apunta a una ruta que no existe (store/link-broken). Con eso, sldb docs update reescribe .sldb/core/store_index.yaml sin 'origin: deskops' en cada modelo de deskops y baja la versión del grafo de aristas. Y sldb models add reescribe los shards de los modelos que no puede importar (los de deskops), borrándoles campos. Un comando sobre documentos propios no debería tocar metadatos de otro store. No está verificado que siga en origin/main 6ab01b80: store_index.yaml todavía guarda 'origin: deskops' por modelo, y desde el 04-11 cambió el layout (sin .sldb/runtime/). La tarea task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de cubre otro disparador (un modelo enlazado que rechaza documentos), no un enlace roto. La pregunta de la nota sobre si el enlace roto es esperado es de la configuración de Chatbot_Infra, no de sldb.

## Goal

_Describe the concrete result this task must produce._

Con un test se sabe si, en un store A con un enlace a un store B cuya ruta no existe, 'docs update' de un documento de A o 'models add' en A cambian alguna entrada de store_index.yaml o algún archivo de modelos o shards que pertenezca a modelos con origin B. Si los cambia, se arregla para que esas entradas queden byte a byte iguales.

## Scope

_State what is in scope and what is out of scope._

Dentro: un test de reproducción en tests/store/ o tests/api/ que crea A y B con la API pública de stores (src/sldb/api/stores/link_store.py), registra en A un modelo con origin B, rompe la ruta del enlace, toma un snapshot de bytes de .sldb/ de A, corre docs update y models add, y compara. Si hay diferencias en entradas de B, el arreglo va en el camino de escritura (src/sldb/api/documents/payload_save.py y los pasos de reconstrucción del índice). CHANGELOG.md. Fuera: reparar el enlace (stores add --replace) y cambiar el formato de store_index.yaml.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test de reproducción. 2) Si no reproduce en origin/main, se deja el test como guardia y se anota en el informe. 3) Si reproduce, conservar las entradas de modelos con origin distinto del local cuando su store no se puede leer. 4) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

El test pasa: tras docs update y models add con el enlace roto, las entradas y archivos de los modelos con origin B quedan iguales; la suite completa sale rc 0.
