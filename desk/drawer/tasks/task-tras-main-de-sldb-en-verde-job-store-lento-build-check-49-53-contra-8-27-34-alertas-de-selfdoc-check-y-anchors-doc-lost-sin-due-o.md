---
id: task-tras-main-de-sldb-en-verde-job-store-lento-build-check-49-53-contra-8-27-34-alertas-de-selfdoc-check-y-anchors-doc-lost-sin-due-o
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

# Tras main de sldb en verde: job store lento (build --check 49:53 contra 8:27), 34 alertas de selfdoc check y anchors/doc_lost sin dueño

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-tras-main-de-sldb-en-verde-job-store-lento-build-check-49-53-contra-8-27-34-alertas-de-selfdoc-check.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-tras-main-de-sldb-en-verde-job-store-lento-build-check-49-53-contra-8-27-34-alertas-de-selfdoc-check.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgos que deja la entrega de main de sldb en verde (wt/main-de-sldb-en-verde 261b8e7f, informe runs/subagents/sldb-ci-worker-report.md), medidos el 2026-11-10 sobre clon limpio de 976519b7. Pasan con rc 0, pero la regla del dueño es que un hallazgo conocido sin tarea no existe.

1. Rendimiento del job store. Paso 6 (sldb stores build --check) tardó 49:53 y paso 7 (sldb stores build && sldb selfdoc check) 26:34. En el CI del 2026-10-20 el paso 6 tardaba 8:27. Hay que medir con el CI (el tiempo local estuvo con otro pytest corriendo en la máquina) y, si se confirma, encontrar qué parte creció (federación de stores enlazados, ver task-reglas-rule-graph-no-compone-la-federación-entera, wt/rule-graph-local) antes de que el job pase el timeout.

2. selfdoc check: ok true y exit 0, pero 34 alertas: 15 selfdoc/untracked, 15 selfdoc/missing, 4 selfdoc/changed. Ninguna sobre los ids --class/--function de f3f9b08c. Hay que clasificarlas: las untracked/missing pueden ser las mismas de python-sync (drawer 40026e8b, símbolos desaparecidos que no se destrackean); las changed, documentos desactualizados respecto al código.

3. anchors/doc_lost en el store de sldb: ReviewDoc cuyo TaskCodeDoc ya no existe (tareas cerradas y destrackeadas por closeout commit; los recibos quedan). Misma causa que la línea base de deskops (drawer de deskops 91cb77db, task-l-nea-base-de-sldb-stores-check-...); se resuelve en deskops closeout, aquí se registra el efecto.

4. Python 3.12 no se verificó localmente; lo verifica el CI de la integración.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
