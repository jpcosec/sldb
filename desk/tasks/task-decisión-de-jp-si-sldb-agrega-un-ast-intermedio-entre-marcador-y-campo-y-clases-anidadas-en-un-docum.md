---
sldb:
  by: agent
  at: '2026-11-16T08:53:55Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- drawer feature-nested-primitive-classes-via-composition (retirado en el triaje 2026-11-16;
  contenido en git antes del commit del triaje)
depends_on: []
pills: []
files:
- docs/architecture/model-authoring.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: drawer feature-decoupled-ast-and-field-instances (retirado en el triaje
  2026-11-16; contenido en git antes del commit del triaje)
---

# Decisión de JP: si sldb agrega un AST intermedio entre marcador y campo y clases anidadas en un documento (dos features del drawer)

## Rationale

_Explain why this task exists or the business driver behind it._

Dos features del drawer piden cambiar el núcleo de extracción. (1) AST desacoplado: un marcador nombraría una forma de AST (por ejemplo un ítem de lista de tareas con estado marcado) que luego se mapea al campo, en lugar del mapeo 1:1 de hoy entre marcador y handler (src/sldb/core/handlers/router.py; src/sldb/core/handlers/list.py solo da strings). (2) Clases anidadas por composición: campos list[SubModelo] extraídos recursivamente de una lista o sección; hoy las tablas dan filas como dicts (src/sldb/core/handlers/table.py:8) y __compositions__ (src/sldb/models/structured_doc.py:13) compone otros documentos, no objetos en línea. Las dos tocan el mismo código y la propia feature 2 pregunta si van juntas. Es una decisión de dirección del núcleo, por eso es del dueño. Origen: feature del drawer feature-decoupled-ast-and-field-instances (retirado en el triaje 2026-11-16) y feature del drawer feature-nested-primitive-classes-via-composition (retirado en el triaje 2026-11-16).

## Goal

_Describe the concrete result this task must produce._

JP decide una de: (a) no se hacen (se retiran las dos features); (b) se hace solo (2), clases anidadas sobre listas y tablas, sin AST intermedio; (c) se hacen las dos juntas. La decisión queda en docs/architecture/model-authoring.md, sección "AST intermedio y clases anidadas", con fecha, y si no es (a) se crea la tarea de diseño correspondiente.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las opciones con costo y quién lo pide hoy: ningún consumidor activo lo pide en el inbox; la tarea task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field toca la misma frontera átomo/field. Recomendación del coordinador: (a) por ahora, y reabrir si la tarea del set bootstrap lo necesita. Registrar el recibo owner (dispose accepted de JP), escribir la sección, y crear con deskops add task la tarea de diseño si corresponde. No entra: implementar ni prototipar.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): si JP elige (a), el coordinador retira las dos features del drawer con deskops drawer remove en el mismo cierre; si elige (b) o (c), las features se retiran cuando exista la tarea de diseño creada (que las cita en references).

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f; JP: "lo que no está marcado no necesita quedar registrado"). Principio en kimun: doc v2 de kimun 00-nucleo.md:55 (5.3) "no todo lo expresado se vuelve conocimiento registrado" y doc v2 de kimun 14-juego-del-lenguaje.md:424,434 "Lo que no selecciona no entra al store ... No hace falta marcar documentos ni subclases para ignorar un párrafo". Objetos anidados: kimun no los incrusta; son documentos aparte referenciados por compositions, "Los documentos referenciados se resuelven por índice, no por embebido" (doc v2 de kimun 07-modelos-como-nodos.md:78), y sus tipos de campo no tienen submodelo incrustado (07:80). El AST con selectores es su diseño objetivo (14:196-206, decisión 28) pero el lenguaje de selectores sigue pendiente (14:208). Recomendación para que JP confirme: (a), no se hacen. Lo anidado se modela como documentos aparte con __compositions__, que sldb ya tiene, y lo que ningún marcador reclama se queda en el archivo sin registrarse. El AST intermedio se reabre solo si la tarea del set bootstrap lo necesita.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer las dos features y docs/architecture/model-authoring.md. 2) Pedir decisión a JP. 3) Escribir la sección. 4) Crear la tarea de diseño o dejar las features para retiro (deskops drawer remove) según la respuesta.

## Validation

_List the checks required before this task can close._

- grep -n 'AST intermedio y clases anidadas' docs/architecture/model-authoring.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea de diseño creada si no es (a); commit del doc.
