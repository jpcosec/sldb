FILE:desk/tasks/task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la.md
---
sldb:
  by: agent
  at: '2026-11-16T06:08:08Z'
  authority: generated
  via: save_document_payload
id: task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-193320-suggestion-ir-pide-exportar-desde-sldb-api-notations-los-modelos-de-spec-de-d3-y-guardar-style-y-entity-en-specdoc.md
depends_on: []
pills: []
files:
- src/sldb/models/notation/spec_doc.py
- src/sldb/api/notations/spec_sync_docs.py
- tests/notations/test_spec_sync.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
---

# SpecDoc guarda los datos de un spec que no son elementos (data.entity y afines) y el style llega a la vista resuelta

## Rationale

_Explain why this task exists or the business driver behind it._

IR11 (specIR, compiladores y proyecciones migrados de spec2viz) necesita que el SpecDoc sincronizado conserve lo que el spec YAML declara además de elementos y aristas. SpecDoc ya guarda style (src/sldb/models/notation/spec_doc.py, campo style) y la sincronización lo escribe (src/sldb/api/notations/spec_sync_docs.py), pero no hay campo para data.entity ni otros datos del spec, así que se pierden al pasar por el store. Origen (pedido 2): desk/inbox/20261115-193320-suggestion-ir-pide-exportar-desde-sldb-api-notations-los-modelos-de-spec-de-d3-y-guardar-style-y-entity-en-specdoc.md.

## Goal

_Describe the concrete result this task must produce._

Sincronizar un spec con data.entity (y cualquier otra clave de data que no sea elementos) y leerlo de vuelta con el SpecDoc devuelve esos datos sin pérdida, y la vista resuelta de ese SpecDoc incluye su style.

## Scope

_State what is in scope and what is out of scope._

Entra: leer primero la nota de origen completa para fijar qué claves de data pide IR11; agregar a SpecDoc un campo opcional data: dict[str, Any] = {} (vacío por defecto) que guarda las claves de data que no son elementos, con render y extract reversibles en la plantilla del modelo; escribirlo en spec_sync_docs.py; comprobar con un test que resolve_view (sldb.api.notations) pasa style a la vista resuelta y, si no lo hace, pasarlo. Tests en tests/notations/test_spec_sync.py (round trip de data.entity) y tests/notations/test_spec_loader.py si hace falta. Los SpecDoc existentes siguen validando (el campo nuevo es opcional); correr sldb stores build --check. CHANGELOG.md. No entra: reexportar clases (tarea de exports de sldb.api.notations), cambiar el formato YAML de los specs, ni migrar SpecDoc del modelo local docs.models:SpecDoc (tarea de decisión aparte).

Precisiones (preflight-1): lo que pide IR11 (pedido 2 de la nota): que SpecDoc guarde, además de style, el data.entity del spec. "Elementos" son las claves de data que ya se sincronizan hoy como nodos y aristas (nodes, edges y las que spec_sync_docs.py ya mapea); toda otra clave de data se guarda en el campo nuevo. El campo es data: dict[str, Any] = Field(default_factory=dict), con un marcador de bloque YAML en la plantilla del modelo igual al que use style en spec_doc.py (copiar su forma). Para style en la vista resuelta, el test comprueba que la vista que devuelve resolve_view para ese SpecDoc tiene una clave style igual al style del SpecDoc. tests/notations/test_spec_loader.py no se toca salvo que un test existente falle por el cambio.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la nota de origen, src/sldb/models/notation/spec_doc.py (campo style cerca de la línea 58 y la plantilla), src/sldb/api/notations/spec_sync_docs.py (línea 67) y el resolvedor de vistas en sldb.api.notations. 2) Agregar el campo y su marcador en la plantilla. 3) Escribirlo en la sincronización. 4) Test de round trip y test de style en la vista resuelta. 5) sldb stores build --check sobre el store del repo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_sync.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_catalog_sync.py
- TMPDIR=/dev/shm sldb stores build --check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

Un spec con data.entity sincronizado y releído conserva entity; la vista resuelta trae style; los tests y stores build --check pasan; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

