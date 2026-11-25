FILE:desk/tasks/task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz.md
---
sldb:
  by: agent
  at: '2026-11-16T06:21:52Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz
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
- docs/architecture/references.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-linked-store-path-references-cannot-resolve-despite-tracked-targets.md
---

# Decisión de JP: arreglar en sldb las referencias por ruta que no resuelven a través de un store enlazado, o cerrarlo como wontfix

## Rationale

_Explain why this task exists or the business driver behind it._

Resolviendo reportes de MEPU en deskops se reprodujo que `sldb edges unresolved` muestra como unknown_path 11 rutas de pills y rituales del Board solo cuando se lee a través de un store enlazado; todas existen y están trackeadas, y el edges unresolved local está vacío. Causa: _resolve (src/sldb/store/edge_index/declared_resolution.py:57-58) solo usa los dueños de ruta cuando store es None, y _owners_by_path (src/sldb/store/edge_index/composition_targets.py:37-49) deja fuera a propósito los documentos de stores enlazados. deskops ya lo esquiva y la nota dice que no hay plan de workaround en sldb. Arreglarlo (resolver la ruta en el espacio del store fuente, con dueños por (store, ruta)) cambia la regla de aislamiento entre stores, por eso es decisión del dueño. Origen: drawer desk/drawer/tasks/task-linked-store-path-references-cannot-resolve-despite-tracked-targets.md.

## Goal

_Describe the concrete result this task must produce._

JP decide (a) arreglar: se crea la tarea de código con test en tests/api/test_unresolved_references.py; o (b) wontfix: queda escrito en docs/architecture/references.md, sección "Rutas a través de un store enlazado", que una ruta relativa se resuelve solo en su store local y por qué.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las dos opciones; recomendación del coordinador: (a), porque el reporte es un falso unknown_path que confunde a quien lee edges unresolved por la federación, y el arreglo mantiene el aislamiento si la clave es (store, ruta). Registrar el recibo owner (dispose accepted de JP) y ejecutar la consecuencia (crear la tarea o escribir la sección). No entra: implementar el arreglo.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): con (a), la tarea creada agrega en tests/api/test_unresolved_references.py un test con dos stores enlazados donde una ruta relativa del store fuente nombra un documento trackeado de ese mismo store y edges unresolved por la federación no lo reporta. Con (b), la sección dice en un párrafo la regla (una ruta relativa se resuelve solo en el store local) y el motivo (aislamiento entre stores). Validation: con (a) basta que exista la tarea; con (b), el grep de la sección.

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f): el grafo federado arma la parte de cada store enlazado con los dueños de ruta de ESE store (src/kimun/surface/edges.cljc:436, store-parts) y después califica sus ids con el nombre del enlace (qualify-node-id, edges.cljc:396-410); una ruta que no resuelve queda como nodo unresolved_path explícito (edges.cljc:344). Los enlaces guardan la ruta relativa al store (doc v2 de kimun 06-superficies-y-cli.md:71). Recomendación para que JP confirme: (a) arreglar. Resolver la ruta relativa de un documento de B con los dueños de B, calificar el id por el enlace como ya hace sldb (store:Model:name) y conservar el aislamiento, porque la clave es (store, ruta).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el ítem del drawer, declared_resolution.py y composition_targets.py. 2) Pedir la decisión. 3) Crear la tarea o escribir la sección en docs/architecture/references.md.

## Validation

_List the checks required before this task can close._

- grep -n 'Rutas a través de un store enlazado' docs/architecture/references.md || ls desk/tasks | grep -i enlazado

## Done When

_Name the observable condition that makes the task complete._

Recibo owner aceptado por JP; existe la tarea de código (a) o la sección del doc (b) commiteada.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

