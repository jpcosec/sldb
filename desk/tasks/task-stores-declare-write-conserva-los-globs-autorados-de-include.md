---
id: task-stores-declare-write-conserva-los-globs-autorados-de-include
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-stores-declare-write-aplana-los-globs-de-include-en-paths-enumerados.md
---

# stores declare --write conserva los globs autorados de include

## Rationale

_Explain why this task exists or the business driver behind it._

Al armar el store central de deskops, 'sldb stores declare --write' reescribió include: convirtiendo cada 'glob: desk/atoms/atom-*.md' en una lista paths: enumerada (93 líneas). La declaración es autorada: el glob es la intención del dueño y la enumeración es derivada. Pedido por deskops el 2026-10-29 (inbox 20261029-005556).

## Goal

_Describe the concrete result this task must produce._

declare --write deja intactas las reglas glob existentes y solo agrega lo que falta (links nuevos, modelos nuevos, documentos que ningún glob cubre); si va a aplanar algo, lo dice y no lo hace sin --flatten o similar.

## Scope

_State what is in scope and what is out of scope._

Código de 'sldb stores declare' (buscar en src/sldb/api/stores/ y src/sldb/cli/commands/stores.py) y sus tests. Sin cambiar el formato de store.yaml ni el comportamiento de stores build.

## Implementation Path

_Outline the expected implementation route or affected surface._

Agente Scion (deskops-executor) implementa con test de regresión: un store.yaml con include glob + un link nuevo -> declare --write conserva el glob y agrega el link.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'declare or stores'

## Done When

_Name the observable condition that makes the task complete._

El test de regresión pasa; reproducir el caso de deskops (cd deskops && sldb stores declare --store .sldb --write) deja el diff de store.yaml solo con lo que faltaba; respuesta enviada al desk de deskops con deskops message send --to deskops.
