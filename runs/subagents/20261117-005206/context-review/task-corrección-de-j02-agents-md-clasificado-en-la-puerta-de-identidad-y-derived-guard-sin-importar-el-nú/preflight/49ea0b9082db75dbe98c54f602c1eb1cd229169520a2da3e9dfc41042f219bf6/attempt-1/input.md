FILE:desk/tasks/task-corrección-de-j02-agents-md-clasificado-en-la-puerta-de-identidad-y-derived-guard-sin-importar-el-nú.md
---
sldb:
  by: agent
  at: '2026-11-17T00:47:03Z'
  authority: generated
  via: create_document
id: task-corrección-de-j02-agents-md-clasificado-en-la-puerta-de-identidad-y-derived-guard-sin-importar-el-nú
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- tools/check_identity.py
- tests/test_store_seams.py
depends_on: []
pills: []
files:
- tools/check_identity.py
- tests/store/test_update_fault_tolerance.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
---

# Corrección de j02: AGENTS.md clasificado en la puerta de identidad y derived_guard sin importar el núcleo fuera de los seams

## Rationale

_Explain why this task exists or the business driver behind it._

El integrador retiene j02 (merge driver y rebuild-index, commit 7dbb6bc9) por dos fallos que su tester no vio: (1) tools/check.sh --fast falla en la puerta identidad con 'ERROR archivo versionado sin clasificar en la raíz: AGENTS.md', porque j02 agregó AGENTS.md en la raíz y tools/check_identity.py no lo tiene en EXEMPT; (2) tests/test_store_seams.py::test_only_the_seams_import_the_core_the_models_or_the_runtime falla con 'io/derived_guard.py: sldb.core.exceptions': el módulo nuevo derived_guard del paquete sldb.store.io importa el núcleo fuera de los seams permitidos.

## Goal

_Describe the concrete result this task must produce._

tools/check.sh --fast y tests/test_store_seams.py pasan con j02 integrado, sin cambiar el comportamiento del merge driver, de rebuild-index ni del error que nombra el comando.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) agregar AGENTS.md a EXEMPT en tools/check_identity.py, con un comentario que diga que es la guía de procedimiento para agentes (merge de .sldb). (2) que el guard de índices derivados no importe sldb.core fuera de los seams: usar la excepción que ya usan los demás módulos de sldb.store.io (leer cómo lo hacen) o mover la importación a un seam permitido según tests/test_store_seams.py; el error y su mensaje no cambian. No entra: cambiar la lista de seams del test ni otros archivos de j02.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/test_store_seams.py y tools/check_identity.py. 2) Ver qué excepción usan los demás módulos de sldb.store.io. 3) Corregir el guard y EXEMPT. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan, incluidos test_store_seams.py y check.sh --fast con todas sus puertas; el error de un índice derivado con marcadores sigue nombrando el comando exacto; commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-corrección-de-j02-agents-md-clasificado-en-la-puerta-de-identidad-y-derived-guard-sin-importar-el-nú: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

