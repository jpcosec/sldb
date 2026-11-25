FILE:desk/tasks/task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar.md
---
sldb:
  by: agent
  at: '2026-11-16T06:18:04Z'
  authority: generated
  via: save_document_payload
id: task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

Precisiones (preflight-1): Validation tiene dos comandos pytest; "los tres comandos" de Done When debe leerse "los dos comandos de Validation". El mensaje del choque es exactamente "module <nombre> already imported from <module.__file__>", con el __file__ del módulo que ya estaba en sys.modules. Este contrato solo detecta y reporta el choque: no lo mitiga (no se cambia la estrategia de import). "Se sabe por qué la raíz enlazada no bastó" se cumple cuando result-summary.md del run dice cuál de los dos tests reproduce el síntoma de deskops (modelo que no importa, o choque en sys.modules) y con qué salida.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/query.py 40-75 y document_payload.py 20-65. 2) Test que falla hoy. 3) Guardar errores y cambiar el mensaje. 4) Test del choque en sys.modules. 5) Informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos de Validation pasan; el test del modelo que no importa ve el mensaje nuevo; el informe dice si el choque de sys.modules reproduce el caso de deskops; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

