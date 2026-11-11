---
id: task-graph-missing-en-el-desk-de-sldb-6-referencias-a-archivos-de-deskops-escritas-como-rutas-locales-en-dos-tareas
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

# graph missing en el desk de sldb: 6 referencias a archivos de deskops escritas como rutas locales en dos tareas

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-graph-missing-en-el-desk-de-sldb-6-referencias-a-archivos-de-deskops-escritas-como-rutas-locales-en.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-graph-missing-en-el-desk-de-sldb-6-referencias-a-archivos-de-deskops-escritas-como-rutas-locales-en.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Al correr 'deskops graph missing --root .' en el desk de sldb (main dba50c74) quedan 6 missing_declared_target que no son de sldb: la tarea task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia nombra los módulos de deskops models run, services closeout_gates y services closure (líneas 45, 46 y 55), y la tarea task-reglas-rule-graph-no-compone-la-federación-entera-de-stores-enlazados-27-s-por-comando-de-deskops nombra los tests de deskops activation_rules y lifecycle_end_to_end (línea 60). Son rutas del repo deskops escritas como si fueran de sldb, así que el grafo las busca en la raíz de sldb. Hoy el CI de sldb no corre graph missing, así que no rompe nada, pero tapa faltantes nuevos. Opciones: reescribir esas líneas con 'deskops edit task' sin ruta de archivo (nombrando módulo y repo), o que graph missing entienda un prefijo de repo (deskops:<ruta>) y lo resuelva en el store enlazado. Hecho cuando graph missing en el desk de sldb da 0.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
