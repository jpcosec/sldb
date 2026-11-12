---
id: task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales
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

# stores check sobre un clon sin build da rc 1 con 2453 errores missing de PythonSymbolDoc generados y tapa los errores reales

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Visto por coord2 el 2026-11-11 al verificar la cadena de desk de sldb: en un checkout limpio de sldb main (ce27c82b), sin correr stores build, 'sldb stores check --store .sldb' da FAIL con 2453 errores, todos PythonSymbolDoc 'missing: tracked at knowledge/symbols/<id>.md, not on disk'. Los documentos de símbolos los genera selfdoc python-sync durante stores build y no están en git, pero el índice los trackea. Consecuencia: stores check es rc 1 en cualquier clon recién hecho o worktree efímero, y un error real de un documento del desk se pierde entre los 2453; hoy hay que comparar a mano contra main limpio para saber si una cadena de desk agrega errores. Relacionado con la nota de inbox sobre las miles de líneas 'Sections rebuild missing de knowledge/symbols' (2026-11-09), que es el mismo origen visto desde las escrituras. Opciones: que stores check trate un documento generado ausente (modelo con generate declarado en store.yaml) como alerta 'generated, run stores build' en lugar de error; o que el índice no trackee los generados fuera del build; o que stores check sin build los omita con un resumen de una línea. Hecho cuando stores check en un clon limpio sin build no da errores por documentos generados ausentes y sí da los errores reales.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
