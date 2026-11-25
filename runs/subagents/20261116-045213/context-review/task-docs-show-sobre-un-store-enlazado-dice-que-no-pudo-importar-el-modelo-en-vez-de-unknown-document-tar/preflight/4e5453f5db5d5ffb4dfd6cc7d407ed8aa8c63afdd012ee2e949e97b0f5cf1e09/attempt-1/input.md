FILE:desk/tasks/task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar.md
---
sldb:
  by: agent
  at: '2026-11-16T04:21:37Z'
  authority: generated
  via: save_document_payload
id: task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar
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
files:
- src/sldb/store/query.py
- src/sldb/api/documents/document_payload.py
- tests/api/test_views_linked.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
from_drawer: desk/drawer/tasks/task-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo.md
---

# docs show sobre un store enlazado dice que no pudo importar el modelo en vez de Unknown document target

## Rationale

_Explain why this task exists or the business driver behind it._

Desde el store central de deskops (enlazado a ../sldb/.sldb), `sldb docs show sldb:ArchitectureNarrativeDoc/arch-code-docstring-indexing --store .sldb` respondió "Unknown document target" cuando lo que fallaba era importar el modelo del store enlazado. _resolve_model_type (src/sldb/store/query.py:47-60) ya prueba la raíz del proyecto enlazado, pero traga toda excepción (except Exception: continue) y devuelve None, así que los documentos de ese modelo desaparecen en silencio y runtime_document (src/sldb/api/documents/document_payload.py:23-37) lanza el genérico _unknown_target (línea 61). Origen: drawer desk/drawer/tasks/task-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo.md.

## Goal

_Describe the concrete result this task must produce._

Cuando el documento pedido existe en el índice pero su modelo no se pudo importar, docs show (y runtime_document) lanza un error que dice "could not import model <Modelo> of store <store>: <excepción original>"; y se sabe, con un test, por qué la raíz enlazada no bastó en el caso de deskops.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) reproducir con un test en tests/api/test_views_linked.py: store A enlaza a store B cuyo modelo importa un módulo que no existe; docs show del documento de B da hoy Unknown document target. (2) Guardar en _resolve_model_type el error de import por modelo (dict modelo -> excepción) en vez de descartarlo, y en document_payload.py, cuando el ref nombra un documento cuyo modelo falló, lanzar el error de Goal. (3) Reproducir también un choque de nombres en sys.modules (dos stores con un paquete del mismo nombre, el caso probable de deskops) y anotar en el informe si es la causa; si lo es, el mensaje lo dice ("module <m> already imported from <ruta>"). CHANGELOG.md. No entra: cambiar la estrategia de import de modelos enlazados más allá del mensaje.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/query.py 40-75 y document_payload.py 20-65. 2) Test que falla hoy. 3) Guardar errores y cambiar el mensaje. 4) Test del choque en sys.modules. 5) Informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan; el test del modelo que no importa ve el mensaje nuevo; el informe dice si el choque de sys.modules reproduce el caso de deskops; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

