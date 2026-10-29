---
id: task-cerrar-task-store-generalize-storecodec-y-storeerror-ya-existen
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
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cerrar TASK-store-generalize: StoreCodec y StoreError ya existen

## Rationale

_Explain why this task exists or the business driver behind it._

TASK-store-generalize.md quedó en la raíz como pedido suelto de otro worktree (iso-lab). src/sldb/store/codec.py y store/exceptions.py existen; el archivo huérfano confunde.

## Goal

_Describe the concrete result this task must produce._

Verificar que los tres acoplamientos que pide retirar (StructuredNLDoc, extract_model_data, core.exceptions dentro de store/) están resueltos vía StoreCodec/RuntimeCodec y StoreError, dejar la evidencia y retirar el archivo.

## Scope

_State what is in scope and what is out of scope._

Solo verificación y evidencia: grep de los imports en src/sldb/store/, tests de codec y excepciones, result-summary.md. Sin cambios de código. git rm TASK-store-generalize.md lo hace el supervisor al cerrar.

## Implementation Path

_Outline the expected implementation route or affected surface._

Agente Scion (template deskops-executor) ejecuta la verificación; el supervisor cierra con deskops closeout commit.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'codec or exceptions or store'

## Done When

_Name the observable condition that makes the task complete._

result-summary.md muestra que store/ no importa StructuredNLDoc ni extract_model_data ni core.exceptions a nivel de módulo, con los tests que lo cubren; TASK-store-generalize.md ya no existe en la raíz.
