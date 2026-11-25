REFORMULACION
Propósito: dar a graph_ui (WS13.1/WS13.2, contrato WS11 §5.4) una puerta pública de lectura que no migre ni reconstruya el store como efecto de un GET. Resultado: en `sldb.api`, `read_store(store) -> StoreLocation` (resuelve como open_store, no llama `migrate_store_layout`, exige layout canónico y lanza `SLDBStoreError` con "store not prepared: run `sldb stores update`", inicia operación nueva con `add_owner_import_roots`/`new_operation`/`new_documents_hash_operation`), `store_is_prepared(store) -> bool` y `extract_payload(model, markdown) -> dict`. Repo: /mnt/ssd/proyectos/SLDB_1 (src/sldb, tests, CHANGELOG, docs/architecture/store-declaration.md). Límites: no tocar open_store ni el significado de `mode="readonly"`, no cambiar graph_ui, no servir esto por `sldb serve`.

AMBIGUEDADES
1. "Validation tiene cuatro comandos (tres pytest y tools/check.sh --fast)" pero Validation lista solo dos pytest: obliga a inventar el tercero.
2. "devuelve False si no existe el store (store_exists) o su store_index.yaml (store_index_path)" y "load_store_index": no se indica módulo ni firma; obliga a inventar imports.
3. "StoreLocation(store_path=..., project_root=...)" sin definir el tipo ni sus campos; obliga a inventar la construcción.
4. "el store de layout viejo se arma copiando lo que hace la fixture": ¿copiar código o importar/parametrizar la fixture? obliga a decidir.
5. "una línea en docs/architecture/ sobre la diferencia" frente a "La línea de doc va en docs/architecture/store-declaration.md"; además `files:` no incluye ese archivo.

DRY-RUN
Lecturas: open_store.py, migration.py (49-75), api/__init__.py, fixture de tests/store/test_legacy_layout_migration.py, tests/api/test_api_stores.py, CHANGELOG.md, store-declaration.md. Cambios previstos: read_store.py (`read_store`, `store_is_prepared`), extract_payload.py, exports/`__all__`, tests, línea de CHANGELOG, línea de doc. Dependencias: `_resolve_store_arg`/`_find_default_store`, `project_root`, `_already_canonical`, `store_exists`/`store_index_path`/`load_store_index`, `add_owner_import_roots`, `new_operation`, `new_documents_hash_operation`, `extract_model_data`. Validaciones futuras: los dos pytest nombrados, tools/check.sh --fast, import de los tres nombres, test de cero escrituras y test de store no preparado.

FUTURO
El commit lo hace el coordinador con `deskops closeout commit`; el ejecutor no hace push. El aviso a graph_ui se envía con `deskops message send --to graph_ui` o, si el repo no está registrado, va como línea en el informe. El informe se escribe en runs/subagents/<run-dir>/result-summary.md. La aceptación final y el cierre son decisión humana.
