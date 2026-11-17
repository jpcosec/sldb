---
sldb:
  by: agent
  at: '2026-11-17T01:37:56Z'
  authority: generated
  via: create_document
id: task-sldb-models-validate-importa-los-modelos-de-deskops-models-como-lo-hacen-extract-y-render-no-module
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-094415-unclear-models-validate-falla-con-no-module-named-deskops-base-para-modelos-deskops-models.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/models.py
- src/sldb/api/model_registry/model_reference.py
- tests/test_cli_v2.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb models validate importa los modelos de deskops.models:* como lo hacen extract y render (No module named deskops.base)

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, sldb models validate PillDoc (y AtomDoc, Task*Doc, ProtoAtomDoc, MaterializationContractDoc) falla con 'Unexpected: No module named deskops.base', mientras extract, render, validate de documentos y docs create sí importan deskops.models:AtomDoc. Parece que models validate resuelve los imports relativos del fuente del modelo contra deskops. en vez de deskops.models.. Origen: desk/inbox/20261116-094415-unclear-models-validate-falla-con-no-module-named-deskops-base-para-modelos-deskops-models.md.

## Goal

_Describe the concrete result this task must produce._

sldb models validate <Modelo> importa el modelo con la misma resolución que extract y render, y valida los modelos de deskops.models:* sin error de import.

## Scope

_State what is in scope and what is out of scope._

Entra: encontrar dónde models validate carga la clase (src/sldb/cli/commands/models.py y src/sldb/api/model_registry/model_reference.py) y hacer que use la misma carga que el resto de comandos; test con un paquete de modelos de prueba en tmp_path que use imports relativos dentro de un subpaquete. CHANGELOG. No entra: los otros huecos de la misma nota (van en la tarea de higiene del CLI).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir con un paquete en tmp_path con imports relativos. 2) Comparar la carga de models validate con la de extract. 3) Unificar. 4) Test en tests/test_cli_v2.py. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_model_metadata_drafts.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; con el deskops instalado en la máquina, sldb models validate PillDoc sobre el store de deskops da rc 0; CHANGELOG y commit; aviso a sldb-ui.
