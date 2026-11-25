FILE:desk/tasks/task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n.md
---
sldb:
  by: agent
  at: '2026-11-16T04:23:46Z'
  authority: generated
  via: save_document_payload
id: task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261102-051843-unclear-falta-lectura-publica-de-store-preparado-sin-open-store-ni-migracion.md
- desk/inbox/20261102-081659-unclear-falta-forma-publica-de-abrir-operacion-de-lectura-sin-open-store.md
- desk/inbox/20261102-141033-unclear-adenda-al-intake-081659-open-store-readonly-sirve-para-ws13-2-sin-ser-api-universal-de-lectura.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/read_store.py
- src/sldb/api/documents/extract_payload.py
- src/sldb/api/__init__.py
- src/sldb/store/migration.py
- tests/api/test_api_stores.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice
---

# Lectura pública sin migrar: read_store abre una operación fresca de solo lectura y rechaza un store no preparado; extract_payload extrae de texto ya leído

## Rationale

_Explain why this task exists or the business driver behind it._

El lector de graph_ui (WS13.1/WS13.2, contrato WS11 §5.4) tiene que leer un store sin migrarlo ni reconstruirlo como efecto de un GET, ver altas y bajas hechas por otro proceso, y rechazar de forma observable un store no preparado. Hoy la única puerta pública es sldb.api.open_store, que llama migrate_store_layout si el store existe (src/sldb/api/stores/open_store.py:37-38) aun con mode="readonly" (ese modo solo controla el fallback al store global). La comprobación de layout canónico es privada (_already_canonical, src/sldb/store/migration.py:63), y graph_ui llama new_operation de sldb.store.runtime_cache_signature y sldb.store.documents_hash, fuera de sldb.api. Además extract_model_data solo está en sldb.runtime.validation (línea 65). Tres notas del inbox piden esto.

## Goal

_Describe the concrete result this task must produce._

sldb.api exporta read_store(store) -> StoreLocation, store_is_prepared(store) -> bool y extract_payload(model, markdown) -> dict; read_store nunca escribe en disco, empieza una operación nueva (ve cambios de otros procesos) y lanza SLDBStoreError con el texto "store not prepared: run `sldb stores update`" si el layout no es canónico.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) src/sldb/api/stores/read_store.py nuevo con read_store(store: str | Path | None = None) que resuelve el store igual que open_store (_resolve_store_arg o _find_default_store("readonly")), NO llama migrate_store_layout, llama store_is_prepared y, si es False, lanza SLDBStoreError con el texto de Goal; si es True llama add_owner_import_roots, new_operation y new_documents_hash_operation y devuelve StoreLocation. (2) store_is_prepared(store) en el mismo módulo: True si store_exists y _already_canonical (se mueve o reexporta desde src/sldb/store/migration.py sin cambiar su lógica). (3) extract_payload(model, markdown) en src/sldb/api/documents/extract_payload.py que llama sldb.runtime.validation.extract_model_data. (4) Export de los tres en sldb.api (__init__ y __all__). (5) Tests: tests/api/test_api_stores.py con un audit hook o comparación de mtimes que prueba cero escrituras al leer un store canónico; un store con layout viejo (fixture de tests/store/test_legacy_layout_migration.py) da SLDBStoreError y queda sin migrar; un documento agregado por otro open_store después del primer read_store aparece en un segundo read_store; extract_payload devuelve lo mismo que extract_model_data. CHANGELOG.md y una línea en docs/architecture/ sobre la diferencia open_store/read_store. No entra: cambiar open_store ni el significado de mode="readonly"; cambiar graph_ui (se le avisa por mensaje al cerrar); servir esto por sldb serve.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/stores/open_store.py, src/sldb/store/migration.py (líneas 49-75), src/sldb/api/__init__.py y la fixture de layout viejo en tests/store/test_legacy_layout_migration.py. 2) Implementar read_store.py y extract_payload.py. 3) Exportar. 4) Tests. 5) tools/check.sh --fast (capas). 6) Al cerrar, deskops message send --to graph_ui avisando los nombres nuevos.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm pytest -q tests/store/test_legacy_layout_migration.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los cuatro comandos de Validation pasan; `python -c "from sldb.api import read_store, store_is_prepared, extract_payload"` funciona; el test de cero escrituras y el de store no preparado pasan; CHANGELOG, doc y commit; mensaje enviado a graph_ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

