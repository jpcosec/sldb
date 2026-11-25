---
id: task-plugins-sobre-sldb-deskops-y-specir
status: deferred
summary: ''
tags:
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

# Plugins sobre sldb: deskops y specIR

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261124-214031-suggestion-plugins-sobre-sldb-deskops-y-specir.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261124-214031-suggestion-plugins-sobre-sldb-deskops-y-specir.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

JP (2026-11-24): empezar a transformar deskops y specIR en plugins sobre sldb.

Estado hoy:
- specIR ya se engancha a sldb sin que sldb lo conozca: `sldb mcp --extension specir.mcp_extension:register` agrega 4 tools read-only (specir_types, specir_nodes, specir_rules, specir_impact) y un batch validator; el server, las tools de escritura, la guarda y el undo son de sldb. Sus extractores leen `sldb.api.code.code_facts` (tree-sitter de sldb) y solo interpretan dominio.
- deskops registra sus modelos en el store global (`deskops bootstrap`) y usa sldb como store, pero no pasa por un punto de extension declarado: es una CLI aparte que llama a sldb.

Lo que habria que definir (plan, no codigo todavia):
1. Un contrato de plugin de sldb: que puede aportar un plugin (modelos/contracts, tools MCP, validadores de batch, reglas, comandos CLI `sldb <plugin> ...`, vistas de surface) y como se descubre (entry points de Python, p. ej. grupo `sldb.plugins`) en vez de `--extension module:register` a mano.
2. Generalizar el punto de extension del MCP (`sldb/mcp/extension.py`) a ese contrato, sin romper `--extension`.
3. Migrar specIR primero (ya esta casi en esa forma): entry point propio, `sldb mcp` lo carga por descubrimiento; `specir mcp` queda como atajo.
4. Despues deskops: que modelos, tags semanticos, reglas y vistas del Board entren como plugin, y que su CLI siga existiendo sobre el mismo contrato.
5. Regla de direccion: sldb nunca importa a un plugin; los plugins dependen de sldb.api y del contrato publico.

Partirlo en DAG con fases al promoverlo a tareas (contrato -> MCP -> specIR -> deskops).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
