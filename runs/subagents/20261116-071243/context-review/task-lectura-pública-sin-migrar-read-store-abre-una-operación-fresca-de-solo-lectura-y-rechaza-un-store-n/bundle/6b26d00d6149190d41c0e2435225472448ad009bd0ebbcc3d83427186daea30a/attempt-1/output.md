REFORMULACION

Nodo ejecutable `task.code` (no agregado) en el repo SLDB_1. Propósito: ofrecer lectura pública de un store sin migrarlo ni reconstruirlo como efecto de un GET, viendo cambios de otros procesos y rechazando stores no preparados. Resultado: `sldb.api` exporta `read_store`, `store_is_prepared` y `extract_payload`, con el comportamiento y el error indicados en Goal. Límites: no cambia `open_store` ni `mode="readonly"`, no toca graph_ui, no se sirve por `sldb serve`; el commit lo hace el coordinador.

AMBIGUEDADES

1. "Validation tiene cuatro comandos (tres pytest y tools/check.sh --fast)" frente a la sección Validation, que solo enumera tres (dos pytest + check.sh). Obligaría a inventar el tercer objetivo pytest.
2. "store_is_prepared(store) -> bool ... devuelve False si no existe el store (store_exists)": no se fija el tipo de `store` ni si acepta `None`/`Path` ni cómo deriva `store_path`. Obligaría a inventar su resolución.
3. "read_store ... resuelve el store igual que open_store" y "add_owner_import_roots, new_operation y new_documents_hash_operation": `open_store.py` no está en el bundle ni se dan módulos/firmas de esos helpers. Obligaría a inventar imports y llamadas.
4. "bajo el encabezado '## 0.1.13 — not released yet'": no se aporta CHANGELOG.md; si el encabezado no existe, obligaría a inventar versión y ubicación.

DRY-RUN

Lecturas: `open_store.py`, `migration.py`, `__init__.py`, fixture de `tests/store/test_legacy_layout_migration.py`, `docs/architecture/store-declaration.md`, `CHANGELOG.md`. Cambios previstos: crear `read_store.py` y `extract_payload.py`; editar `__init__.py`/`__all__`; añadir tests en `tests/api/test_api_stores.py`; línea en CHANGELOG y doc. Dependencias: `_resolve_store_arg`/`_find_default_store`, `add_owner_import_roots`, `new_operation`, `new_documents_hash_operation`, `store_exists`/`store_index_path`/`load_store_index`, `_already_canonical`, `project_root`, `StoreLocation`, `SLDBStoreError`, `extract_model_data`, fixture `api_store`. Validaciones futuras: los pytest listados (o cuatro según preflight), `tools/check.sh --fast` y el import de los tres nombres.

FUTURO

El nodo de ejecución produce código, tests, `runs/subagents/<run-dir>/result-summary.md` y el aviso a graph_ui (o su línea en el informe si el repo no está registrado). El coordinador ejecuta `deskops closeout commit` y el closeout verifica tests, commit y árbol limpio.
