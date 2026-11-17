---
sldb:
  by: agent
  at: '2026-11-17T01:42:28Z'
  authority: generated
  via: create_document
id: task-sldb-stores-remove-quita-el-enlace-también-de-la-declaración-store-yaml-así-otra-sesión-no-lo-reintr
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-172753-suggestion-sldb-stores-remove-no-quita-el-enlace-de-la-declaraci-n-en-store-yaml-y-otra-sesi-n-lo-reintroduce.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/unlink_store.py
- tests/api/test_unlink_store.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb stores remove quita el enlace también de la declaración store.yaml, así otra sesión no lo reintroduce

## Rationale

_Explain why this task exists or the business driver behind it._

En deskops, sldb stores remove spec2viz editó solo .sldb/core/store_index.yaml y dejó links: spec2viz en .sldb/store.yaml; otra sesión regeneró el índice desde store.yaml y el enlace volvió. Lo coherente fue remove seguido de stores declare --write. Origen: desk/inbox/20261116-172753-suggestion-sldb-stores-remove-no-quita-el-enlace-de-la-declaraci-n-en-store-yaml-y-otra-sesi-n-lo-reintroduce.md.

## Goal

_Describe the concrete result this task must produce._

sldb stores remove <alias> deja el enlace fuera del índice y de la declaración store.yaml en una sola operación, bajo el lock del store; un store sin store.yaml se comporta como hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/api/stores/unlink_store.py, quitar también la entrada de links de store.yaml (reutilizando la escritura de la declaración que ya usa declare --write, sin reescribir el resto del archivo); test en tests/api/test_unlink_store.py que verifica que tras remove y un update desde la declaración el enlace no vuelve. CHANGELOG. No entra: otros subcomandos de stores.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer unlink_store.py y cómo se escribe store.yaml (declaration_sync y declare). 2) Implementar. 3) Test. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_unlink_store.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_declare_store_authored.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; CHANGELOG y commit; aviso a deskops.
