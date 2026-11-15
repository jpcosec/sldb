---
sldb:
  by: agent
  at: '2026-11-15T15:52:20Z'
  authority: generated
  via: create_document
id: task-sldb-escucha-suscripciones-y-stream-de-eventos-de-escritura-inbox-20261114-115028
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
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb escucha: suscripciones y stream de eventos de escritura (inbox 20261114-115028)

## Rationale

_Explain why this task exists or the business driver behind it._

Idea de JP 2026-11-14: que sldb pueda estar escuchando mensajes; hoy nadie reacciona a una nota hasta que una sesión la lee.

## Goal

_Describe the concrete result this task must produce._

Decidir la forma antes de implementar y dejar la implementación como tareas.

## Scope

_State what is in scope and what is out of scope._

Nota del inbox sldb 20261114-115028. Preguntas a cerrar: si el evento sale de la escritura (Transaction, guardado de payload) o de mirar el árbol (git, inotify), dado que muchos mensajes llegan por git pull; dónde se declara la suscripción (ViewDoc, RuleDoc con un momento nuevo o un modelo propio); exposición por la API pública y por sldb serve (SSE). Se cruza con el log de señales del MCP (tarea sldb mcp) y con la brecha del journal (tarea de brechas de IR01, inbox 20261114-074447): decidir si un solo stream de eventos sirve a los tres. sldb no ejecuta agentes, solo emite el evento.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Decisión escrita con alternativas y tareas de implementación creadas con deskops.
