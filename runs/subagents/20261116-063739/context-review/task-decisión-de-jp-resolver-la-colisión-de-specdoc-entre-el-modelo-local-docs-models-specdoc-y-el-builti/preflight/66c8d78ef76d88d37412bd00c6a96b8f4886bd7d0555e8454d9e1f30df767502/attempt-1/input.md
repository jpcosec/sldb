FILE:desk/tasks/task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti.md
---
sldb:
  by: agent
  at: '2026-11-16T05:23:26Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261106-152834-unclear-specdoc-el-modelo-local-docs-models-specdoc-colisiona-con-el-builtin-sldb-models-notation-models-specdoc-tras-sv01.md
depends_on: []
pills: []
files:
- docs/architecture/notations-and-views.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decisión de JP: resolver la colisión de SpecDoc entre el modelo local docs.models:SpecDoc y el builtin de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Desde SV01 (6b80df36) sldb.models exporta un SpecDoc builtin (src/sldb/models/notation/spec_doc.py, exportado en sldb.api), pero el store de este repo sigue enlazando el nombre SpecDoc a docs.models:SpecDoc (.sldb/store.yaml, líneas 17-18; clase en docs/models.py:237). deskops doctor lo reporta como alerta y cualquier consumidor que resuelva SpecDoc por nombre (sldb serve, graph_ui, deskops view) puede recibir el modelo equivocado. La tarea task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con está relacionada (mueve los specs de docs/architecture/spec2viz) pero no decide esto. Origen: desk/inbox/20261106-152834-unclear-specdoc-el-modelo-local-docs-models-specdoc-colisiona-con-el-builtin-sldb-models-notation-models-specdoc-tras-sv01.md.

## Goal

_Describe the concrete result this task must produce._

JP elige una opción y queda escrita en docs/architecture/notations-and-views.md, sección "SpecDoc local frente al builtin", con la fecha; se crea con deskops add task la tarea de código que la implementa.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones de la nota con su costo: (a) renombrar el modelo local (por ejemplo a ArchitectureSpecDoc) y migrar sus documentos con sldb (costo bajo, sin cambio de semántica); (b) borrar el modelo local y migrar sus documentos al builtin (requiere que el builtin cubra sus campos; costo medio); (c) una regla explícita de precedencia local sobre builtin en la resolución por nombre (cambia sldb para todos los stores; costo alto). Recomendación del coordinador: (a). Registrar el recibo owner (el dispose accepted es de JP), escribir la sección y crear la tarea de implementación con archivos y validación (sldb stores build --check y deskops doctor sin la alerta). No entra: implementar la opción elegida en esta tarea.

Precisiones (preflight-1): las tres opciones son las de este contrato (la nota de origen las enumera igual). Conteo: `sldb stores check --store .sldb` no cuenta por modelo; se usa el índice: el documents_count de .sldb/core/models/SpecDoc.yaml (leerlo con sldb, por ejemplo sldb docs list --model SpecDoc si existe, o contando las entradas de ese modelo en la salida de `sldb docs list`). La tarea de implementación que se crea tiene como validación `TMPDIR=/dev/shm sldb stores build --check --store .sldb` y `TMPDIR=/dev/shm deskops doctor --root sldb` sin la alerta "SpecDoc: another class under the name of the model".
Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/models.py (clase SpecDoc, línea 237), src/sldb/models/notation/spec_doc.py y .sldb/store.yaml 10-25. 2) Contar documentos del modelo local con sldb docs list o sldb stores check. 3) Pedir la decisión a JP con el conteo. 4) Escribir la sección y crear la tarea de código.

## Validation

_List the checks required before this task can close._

- grep -n 'SpecDoc local frente al builtin' docs/architecture/notations-and-views.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción elegida y la fecha; recibo owner aceptado por JP; la tarea de implementación existe en desk/tasks; commit del doc.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

