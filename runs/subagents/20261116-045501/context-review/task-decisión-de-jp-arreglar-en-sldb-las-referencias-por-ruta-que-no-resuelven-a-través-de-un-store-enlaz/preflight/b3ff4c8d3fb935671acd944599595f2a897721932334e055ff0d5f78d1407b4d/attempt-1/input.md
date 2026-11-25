FILE:desk/tasks/task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz.md
---
sldb:
  by: agent
  at: '2026-11-16T04:14:53Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz
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

