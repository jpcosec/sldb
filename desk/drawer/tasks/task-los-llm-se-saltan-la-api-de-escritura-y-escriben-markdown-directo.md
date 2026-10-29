---
id: task-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo
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

# Los LLM se saltan la API de escritura y escriben Markdown directo

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261001-031226-suggestion-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261001-031226-suggestion-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Diagnóstico: el render es demasiado natural, parece la cosa y no una proyección; escribirlo cuesta una llamada y la API cuesta descubrimiento sin dar nada visible a cambio; el archivo no se queja y la divergencia aparece después en stores check. Cambiar la economía, no las instrucciones: (a) hook PreToolUse sobre Write/Edit que bloquee rutas trackeadas por el store y escriba en el error el comando correcto; (b) sldb docs register <ruta> o POST /docs con markdown que extraiga, valide, rechace ruido estructural, indexe y devuelva el render canónico con diff (el invariante es nada entra sin pasar por extract→render, no nadie escribe Markdown); (c) CLAUDE.md en la raíz y la skill de src/sldb/assets/skills/sldb.md cargándose sola cuando hay .sldb/, como deskops-workflow con desk/. Orden: hook, luego register.

## Avance (2026-10-18)

Sigue abierta: no hay hook PreToolUse ni `docs register`. `POST /docs` (4c3c2e0e) existe, pero recibe un payload JSON, no markdown, y no devuelve el render ni el diff.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
