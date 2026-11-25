FILE:desk/tasks/task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum.md
---
sldb:
  by: agent
  at: '2026-11-16T04:18:52Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/features/feature-nested-primitive-classes-via-composition.md
depends_on: []
pills: []
files:
- docs/architecture/model-authoring.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/features/feature-decoupled-ast-and-field-instances.md
---

# Decisión de JP: si sldb agrega un AST intermedio entre marcador y campo y clases anidadas en un documento (dos features del drawer)

## Rationale

_Explain why this task exists or the business driver behind it._

Dos features del drawer piden cambiar el núcleo de extracción. (1) AST desacoplado: un marcador nombraría una forma de AST (por ejemplo un ítem de lista de tareas con estado marcado) que luego se mapea al campo, en lugar del mapeo 1:1 de hoy entre marcador y handler (src/sldb/core/handlers/router.py; src/sldb/core/handlers/list.py solo da strings). (2) Clases anidadas por composición: campos list[SubModelo] extraídos recursivamente de una lista o sección; hoy las tablas dan filas como dicts (src/sldb/core/handlers/table.py:8) y __compositions__ (src/sldb/models/structured_doc.py:13) compone otros documentos, no objetos en línea. Las dos tocan el mismo código y la propia feature 2 pregunta si van juntas. Es una decisión de dirección del núcleo, por eso es del dueño. Origen: desk/drawer/features/feature-decoupled-ast-and-field-instances.md y desk/drawer/features/feature-nested-primitive-classes-via-composition.md.

## Goal

_Describe the concrete result this task must produce._

JP decide una de: (a) no se hacen (se retiran las dos features); (b) se hace solo (2), clases anidadas sobre listas y tablas, sin AST intermedio; (c) se hacen las dos juntas. La decisión queda en docs/architecture/model-authoring.md, sección "AST intermedio y clases anidadas", con fecha, y si no es (a) se crea la tarea de diseño correspondiente.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las opciones con costo y quién lo pide hoy: ningún consumidor activo lo pide en el inbox; la tarea task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field toca la misma frontera átomo/field. Recomendación del coordinador: (a) por ahora, y reabrir si la tarea del set bootstrap lo necesita. Registrar el recibo owner (dispose accepted de JP), escribir la sección, y crear con deskops add task la tarea de diseño si corresponde. No entra: implementar ni prototipar.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer las dos features y docs/architecture/model-authoring.md. 2) Pedir decisión a JP. 3) Escribir la sección. 4) Crear la tarea de diseño o dejar las features para retiro (deskops drawer remove) según la respuesta.

## Validation

_List the checks required before this task can close._

- grep -n 'AST intermedio y clases anidadas' docs/architecture/model-authoring.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea de diseño creada si no es (a); commit del doc.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

