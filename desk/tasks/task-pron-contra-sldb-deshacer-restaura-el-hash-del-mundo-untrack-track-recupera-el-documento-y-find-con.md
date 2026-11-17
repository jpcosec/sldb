---
sldb:
  by: agent
  at: '2026-11-17T01:52:43Z'
  authority: generated
  via: save_document_payload
id: task-pron-contra-sldb-deshacer-restaura-el-hash-del-mundo-untrack-track-recupera-el-documento-y-find-con
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-053107-unclear-pron-contra-sldb-9f27733f-undo-no-restaura-el-hash-del-mundo-y-track-untrack-pierde-el-documento-table-77.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/document_lookup.py
- tests/api/test_transaction.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# pron contra sldb: deshacer restaura el hash del mundo, untrack + track recupera el documento y find con where en un mundo solo vuelve a encontrar

## Rationale

_Explain why this task exists or the business driver behind it._

pron (suite completa contra sldb 9f27733f: 7 fallas) reporta tres síntomas que no puede arreglar sin sldb: (1) al deshacer una escritura, el sello de procedencia queda en el documento y hash_after no vuelve al anterior (goldens test_16_golden_*); (2) tras untrack + track, find_doc (src/sldb/api/documents/document_lookup.py) lanza Doc 'table-77' not found; (3) find de Reservation con where 'doc ~ "ana"' devuelve 0 en un mundo solo. Pide saber si es regresión de sldb o un cambio de contrato que pron debe adoptar. Origen: desk/inbox/20261116-053107-unclear-pron-contra-sldb-9f27733f-undo-no-restaura-el-hash-del-mundo-y-track-untrack-pierde-el-documento-table-77.md.

## Goal

_Describe the concrete result this task must produce._

Cada uno de los tres síntomas queda clasificado con evidencia como regresión de sldb (y arreglado aquí con test) o como cambio de contrato (documentado en el CHANGELOG, con la forma que pron debe adoptar), y las pruebas de pron nombradas en la nota pasan contra este sldb salvo las que dependan de un cambio de contrato que pron deba adoptar.

## Scope

_State what is in scope and what is out of scope._

Entra: reproducir en /dev/shm con un clon de jpcosec/pron (master) y un venv con este sldb editable (como en la tarea del CI de track --force), corriendo PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p syrupy las pruebas de mundo 04 y 10 y los goldens de pron; buscar con git bisect o lectura el commit de sldb que cambió cada comportamiento; arreglar en sldb lo que sea regresión, con test en sldb; documentar lo que sea contrato. Para (1): un deshacer por apply_batch(report.inverse) puede dejar distinto el sello sldb.by/at/via (contrato del lote inverso); si pron deshace por otro camino, decidir con evidencia. No entra: cambiar pron.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir. 2) Clasificar cada síntoma con bisect o lectura. 3) Arreglar las regresiones con test. 4) Validation y repetir la reproducción. 5) result-summary.md con la tabla síntoma -> causa -> regresión o contrato -> commit o texto para pron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md trae la tabla de los tres síntomas con su evidencia y la reproducción de pron antes y después; CHANGELOG y commit si hubo arreglo; respuesta a pron por su inbox.
