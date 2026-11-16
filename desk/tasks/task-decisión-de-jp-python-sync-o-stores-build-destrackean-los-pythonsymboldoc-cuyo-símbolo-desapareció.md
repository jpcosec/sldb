---
sldb:
  by: agent
  at: '2026-11-16T08:49:01Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció
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
- docs/self-documentation.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: drawer task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci
  (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)
---

# Decisión de JP: python-sync o stores build destrackean los PythonSymbolDoc cuyo símbolo desapareció

## Rationale

_Explain why this task exists or the business driver behind it._

selfdoc python-sync escribe PythonSymbolDoc pero nunca destrackea (write_python_plans, src/sldb/cli/commands/selfdoc_python.py:69; no hay untrack en src/sldb/selfdoc). El contrato actual los conserva a propósito: src/sldb/selfdoc/report.py:32 "Removed documents are retained" y el test tests/selfdoc/test_sync.py::test_removed_commands_are_reported_and_retained. Resultado: cuando c420809c borró el journal quedaron 108 PythonSymbolDoc huérfanos (stores build en sitio: undeclared 108), limpiados a mano con sldb docs untrack (dfa5c504; otro en 641ecdfa). Destrackear cambia la semántica (borra documentos trackeados derivados), por eso es del dueño. Origen: drawer desk/drawer/tasks/task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci.md.

## Goal

_Describe the concrete result this task must produce._

JP decide (a) python-sync destrackea los PythonSymbolDoc de su system cuyo símbolo ya no existe y conserva los documentos de comandos y superficies escritos por personas; (b) también destrackea los de comandos y superficies; o (c) se mantiene la retención y solo se reportan. La decisión queda en docs/self-documentation.md, sección "Símbolos que desaparecen", y si es (a) o (b) se crea la tarea de código que cambia report.py y test_sync.py.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones; recomendación del coordinador: (a), porque los PythonSymbolDoc son generados (knowledge/symbols/ está en derived) y los de comandos y superficies los escriben personas. Registrar el recibo owner (dispose accepted de JP), escribir la sección, crear la tarea de código si corresponde. No entra: implementar; la alerta de stores check sobre documentos derivados ausentes es otra tarea.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): generado = PythonSymbolDoc (el modelo que escribe python-sync bajo knowledge/symbols/, ruta declarada derived); escritos por personas = los documentos de comandos y superficies que selfdoc reporta como removed pero que no están bajo una ruta derived. El recibo se verifica con `deskops review status <esta tarea> --root sldb`.

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f): "Regla de untrack. Un símbolo que desaparece del código no borra su documento: sync hace docs untrack y el archivo queda en disco" (doc v2 de kimun 11-adaptadores.md:217-218). Es un cambio explícito sobre v1, que "solo informaba removed": check informa orphan con exit 1 (11:449-450). Si el símbolo vuelve, "su archivo retenido se adopta y sus campos autorados sobreviven" (11:222-230). El alcance es solo lo que el adaptador posee: etiqueta del adaptador, system y directorio de salida (11:189-198). Principio: "Si es borrado, no se mantiene el nodo ... si se borra un ID estructural que soporta un claim de conocimiento, se declara" (14-juego-del-lenguaje.md:513-515). Recomendación para que JP confirme: (a). python-sync destrackea los PythonSymbolDoc de su system cuyo símbolo desapareció y deja el archivo en disco; selfdoc check los informa como orphan; si el símbolo vuelve, el documento se re-adopta. Los documentos de comandos y superficies escritos por personas no se tocan.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer report.py, selfdoc_python.py, tests/selfdoc/test_sync.py y docs/self-documentation.md. 2) Pedir decisión. 3) Escribir la sección. 4) Crear la tarea de código con validación TMPDIR=/dev/shm pytest -q tests/selfdoc/test_sync.py.

## Validation

_List the checks required before this task can close._

- grep -n 'Símbolos que desaparecen' docs/self-documentation.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea de código creada si es (a) o (b); commit del doc.
