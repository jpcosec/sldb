---
id: task-sw13-lado-derecho-de-la-barra-superior-del-workbench-es-dif-cil-de-manejar
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW13 · Lado derecho de la barra superior del Workbench: es difícil de manejar.

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261117-131231-suggestion-sw13-lado-derecho-de-la-barra-superior-del-workbench-es-dif-cil-de-manejar.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261117-131231-suggestion-sw13-lado-derecho-de-la-barra-superior-del-workbench-es-dif-cil-de-manejar.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

SW13 · Lado derecho de la barra superior del Workbench: es difícil de manejar.
Comentario de JP, textual: "Esto de aca esta un poco dificil de manejar". Elemento señalado: div.wb-topbar-right en surface/src/app/WorkbenchShell.tsx:353 en adelante. Lo que contenía al comentar: "Lectura · [ Estructura / Fierros ] · Esquema", "Fuente ↗", "contrato InboxNoteDoc ↗", "[ Sincronizado con .sldb ]" y "⌘K".
Qué pasa hoy: en una sola fila conviven cinco cosas de naturaleza distinta, todas como texto mono del mismo tamaño y peso: tres lentes (un selector), dos enlaces que cambian de vista y cuyo rótulo cambia según la vista (en anclaje dice "leer fuente ↗"), un indicador de estado que no es un control y el atajo de la paleta. No se distingue qué es selector, qué es navegación y qué es estado.
Qué pide: JP no dio una solución, solo el problema. La tarea parte por un contrato que proponga el orden (por ejemplo: lentes como un grupo, navegación entre vistas en otro lugar, estado separado) y lo confirme con JP con capturas antes de implementar.
Puntos a resolver: si los enlaces de vista (Fuente, contrato) pertenecen a la barra o al documento; qué pasa en anchos chicos; que el teclado (1, 2, 3, ⌘K) siga igual; no agregar color ni cajas que rompan "papel con fierros ocultables".
Antecedente: al capturar este comentario impeccable alcanzó a preparar un envoltorio de variantes sobre este bloque; no se escribió nada en el código (sourceWritten: false).
done_when sugerido: JP aprueba una disposición sobre capturas en las cuatro vistas y a 1440 y 1024 px; los tests de lentes y de navegación siguen pasando.
Toca WorkbenchShell.tsx: en serie con las demás tareas que tocan ese archivo.

Origen: comentario que JP dejó sobre la propia interfaz al recorrer el Workbench de sldb/surface (2026-11-17, vía la sesión supervisora local). Instrucción de JP: cada comentario se registra como tarea, no se resuelve en el momento. Base de código: df3903db en origin/main de sldb. Contexto de producto: el Workbench es LA UI de SLDB, general y autónoma; principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Va en la cola después de la serie SW1-SW9, salvo que JP diga otra cosa. La evidencia viene de lectura del código; confirmar cada punto antes de escribir el TaskDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
