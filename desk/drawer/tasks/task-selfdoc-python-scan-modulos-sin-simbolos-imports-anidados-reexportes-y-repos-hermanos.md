---
id: task-selfdoc-python-scan-modulos-sin-simbolos-imports-anidados-reexportes-y-repos-hermanos
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

# selfdoc python-scan: módulos sin símbolos, imports anidados, reexportes y repos hermanos

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261122-185316-suggestion-selfdoc-python-scan-m-dulos-sin-s-mbolos-imports-anidados-reexportes-y-repos-hermanos.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261122-185316-suggestion-selfdoc-python-scan-m-dulos-sin-s-mbolos-imports-anidados-reexportes-y-repos-hermanos.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de Chatbot_Infra en el triaje del 2026-11-22: es un pedido para sldb que quedó escrito allá con sldb inbox el 2026-11-04 y nunca llegó a este desk. Texto original: Al armar el mapa de código de la wiki del desk (ops/wiki_desk.py) con sldb selfdoc python-scan faltó: (1) un módulo sin clases ni funciones (p. ej. un __init__ que solo reexporta) no aparece en la salida, así que no se ven sus imports; (2) solo se ven los imports de nivel de módulo, no los de dentro de una función; (3) no resuelve reexportes: from data import SqlStore queda como uso de data/__init__ y no de data/store.py, ni los reexportes perezosos por un mapa de nombres; (4) --source-root tiene que estar dentro del proyecto del store: un repo hermano (../labchile_chatbots) se escanea con su propio store; (5) para tener el grafo node-link hay que usar python-sync, que trackea un documento por símbolo (miles). Sugerencia: python-scan --graph-output sin trackear, con nodos de módulo para todo archivo .py y aristas resueltas a través de reexportes. Mientras tanto la herramienta lo completa con ast.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
