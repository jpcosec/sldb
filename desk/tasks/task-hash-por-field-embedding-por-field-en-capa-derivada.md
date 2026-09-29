---
id: task-hash-por-field-embedding-por-field-en-capa-derivada
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-hash-por-field-embedding-por-field-en-capa-derivada
current_node: checklist-task-hash-por-field-embedding-por-field-en-capa-derivada-closeout-ready
history:
- operator-task-hash-por-field-embedding-por-field-en-capa-derivada-activate
- operator-task-hash-por-field-embedding-por-field-en-capa-derivada-ready-for-testing
references:
- desk/drawer/tasks/task-ast-parse-hotspots-re-parseo-duplicado-y-markdownit-no-reusado.md
- desk/atoms/atom-un-mapa-de-hashes-vacio-significa-no-se-pudo-calcular-nunca-nada-cambio.md
- e823570f3b4e4cd90da3ac859c66a167dbf75148
- 9976efc79a6fa877b09dfaf0d18c5236641e73ed
- tests/store/test_documents_shards.py
- tests/test_serve.py
- tests/test_runtime_cache.py
- tests/test_clean_code_rules.py
- desk/drawer/tasks/task-hash-por-field-embedding-por-field-en-capa-derivada.md
depends_on: []
pills: []
files:
- docs/user-manual.md
- src/sldb/api/documents/payload_save_steps.py
- src/sldb/api/model_registry/model_index_writes.py
- src/sldb/api/stores/index_refresh.py
- src/sldb/cli/commands/doc.py
- src/sldb/store/__init__.py
- src/sldb/store/diagnostics.py
- src/sldb/store/diagnostics_models/document_diagnosis.py
- src/sldb/store/hashing.py
- src/sldb/store/models/document_entry.py
- src/sldb/store/ops.py
checklists:
- checklist-task-hash-por-field-embedding-por-field-en-capa-derivada-execution-ready
- checklist-task-hash-por-field-embedding-por-field-en-capa-derivada-testing-ready
- checklist-task-hash-por-field-embedding-por-field-en-capa-derivada-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-mapa-de-hashes-vacio-significa-no-se-pudo-calcular-nunca-nada-cambio
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Hash por field en DocumentEntry (paso 1 de field-level indexing)

## Rationale

_Explain why this task exists or the business driver behind it._

El Merkle tree del store llega al documento, no al field. `content_hash` es un
sha256 del JSON completo del payload, asi que cambiar 1 field de 40 invalida el
documento entero y `stores check` no puede atribuir un mismatch a un field.
Es ademas el prerrequisito del embedding por field: sin hash por field,
`DocumentIndex._partition` re-embeberia todos los fields de un documento cada
vez que cambia uno.

## Goal

_Describe the concrete result this task must produce._

Emitir y persistir un hash por field junto al `content_hash` existente, sin alterar la semantica de `content_hash`.

## Scope

_State what is in scope and what is out of scope._

INCLUYE:
- `hash_field_map(model_type, markdown_text, codec)` en `store/hashing.py`,
  reusando `codec.extract` y `hash_payload`.
- Campo `field_hashes: dict[str, str] = {}` en `DocumentEntry`
  (default vacio => stores viejos siguen cargando).
- Propagacion en los 8 write-sites que hoy llaman `hash_fields()`:
  cli/commands/doc.py:59, cli/selfdoc_registry.py:70, store/ops.py:80,
  store/diagnostics.py:46, api/model_drafts/backfill.py:101,
  api/model_registry/model_index_writes.py:62,
  api/stores/index_refresh.py:77, api/documents/payload_save_steps.py:68.
- Punto natural de calculo: `_field_hash` en `api/stores/index_refresh.py`,
  que ya cachea el payload extraido.
- Atribucion por field en el finding `data_mutation` de `stores check`.

NO INCLUYE (tarea siguiente):
- Embeddings por field / `DocumentIndex` con key `Model/doc#field`.
- Cualquier cambio a la capa de matching.

NO-GOAL explicito:
- NO tocar la semantica de `content_hash`: es el token de concurrencia
  optimista de `/save` (`expected` => 409). `field_hashes` va AL LADO, no se
  deriva uno del otro ni se reemplaza.
- NO reemplazar hashes por embeddings (evaluado y descartado: no es exacto,
  no es determinista entre versiones de modelo, no compone en el Merkle).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `store/hashing.py`: agregar `hash_field_map`. Costo marginal medido:
   24 us/doc para 12 fields sobre payload ya extraido (24 ms / 1000 docs).
2. `store/models/document_entry.py`: agregar `field_hashes`, default `{}`.
3. `api/stores/index_refresh.py`: calcular el map donde ya se resuelve el
   payload (`_field_hash`), evitando una segunda extraccion.
4. Propagar en los write-sites restantes.
5. `store/diagnostics.py`: que `data_mutation` liste los fields que cambiaron
   comparando el map en indice vs el recalculado.
6. Migracion: seguir el precedente de `store/migration_hash_names.py`
   (backfill perezoso; un store sin `field_hashes` se completa en su proximo
   write, sin invalidar nada).

## Validation

_List the checks required before this task can close._

- python -m pytest tests/ -q
- python -m pytest tests/store/ tests/test_serve.py tests/test_runtime_cache.py -q
- python -m sldb stores check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

- `hash_field_map` existe y es funcion pura del payload (mismo payload =>
  mismo map).
- `DocumentEntry.field_hashes` se persiste y se relee; un store creado ANTES
  del cambio carga sin error con `field_hashes == {}`.
- `content_hash` conserva exactamente su valor y su rol: el test de 409 en
  `/save` con `expected` sigue verde sin modificarse.
- `stores check` ante una mutacion de 1 field nombra ESE field en el finding.
- Suite completa verde.
