FILE:desk/tasks/task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com.md
---
sldb:
  by: agent
  at: '2026-11-16T04:27:44Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md
depends_on: []
pills: []
files:
- docs/architecture/views.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
---

# Decisión de JP: qué de las vistas de deskops (H1-H8 de CC34) expresa la ViewDoc de sldb y qué queda como agregado del consumidor

## Rationale

_Explain why this task exists or the business driver behind it._

deskops view board|task salen de sldb.api.run_view proyectado al contrato de el doc deskops-ui.md del repo deskops. Lo que la ViewDoc no expresa lo completa el CLI de deskops con lecturas existentes, marcadas "pendiente de sldb Hn". CC34 listó ocho cosas: (H1) transitions.from_field necesita export id; (H2) transitions admite una sola relation y el ciclo tiene tres; (H3) gates con holds=false no aparecen; (H4) closeout no tiene fuente sin recibos evidence; (H5) next sale del spec yaml del paquete; (H6) pills/atoms/validation efectivos por herencia no están en el índice; (H7) el texto crudo del drawer no está en las filas; (H8) no hay revision por nota del inbox. La nota pide que la ViewDoc las exprese o una decisión explícita de que quedan del lado del consumidor. Es una decisión de alcance del modelo ViewDoc (sldb) frente a deskops, por eso es del dueño. Origen: desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md.

## Goal

_Describe the concrete result this task must produce._

JP decide, para cada una de H1-H8, "sldb" (la ViewDoc lo expresa y se crea una tarea de código en sldb) o "consumidor" (deskops lo agrega fuera de run_view y quita la marca "pendiente de sldb Hn"); la decisión queda escrita en docs/architecture/views.md, sección "Decisión H1-H8 (CC34)", con la fecha y una línea por hipótesis.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las ocho hipótesis con esta recomendación del coordinador: H1, H2 y H3 a sldb (son del modelo de transiciones que ya vive en sldb: export id en from_field, varias relations, gates no sostenidos); H4-H8 al consumidor (dependen de recibos, specs de paquete, herencia y archivos no trackeados que son de deskops, en línea con el atom atom-sldb-evaluates-declared-rules-consumers-author-them). Registrar su respuesta en docs/architecture/views.md, crear con deskops add task una tarea de código en sldb por cada H que quede en "sldb", y mandar a deskops con deskops message send --to deskops la lista de las que quedan del consumidor. No entra: implementar nada; H9-H13 (resueltas o en otra tarea).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/views.md y la nota de origen. 2) Pedir la decisión a JP (registrar el recibo owner con deskops review record <tarea> --kind owner; el dispose accepted lo hace JP). 3) Escribir la sección en views.md. 4) Crear las tareas resultantes y mandar el mensaje a deskops. 5) Commit del doc.

## Validation

_List the checks required before this task can close._

- grep -n 'Decisión H1-H8 (CC34)' docs/architecture/views.md

## Done When

_Name the observable condition that makes the task complete._

views.md tiene la sección con las ocho líneas; existe una tarea en desk/tasks por cada H decidida "sldb"; deskops recibió el mensaje; recibo owner aceptado por JP; commit con el doc.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

