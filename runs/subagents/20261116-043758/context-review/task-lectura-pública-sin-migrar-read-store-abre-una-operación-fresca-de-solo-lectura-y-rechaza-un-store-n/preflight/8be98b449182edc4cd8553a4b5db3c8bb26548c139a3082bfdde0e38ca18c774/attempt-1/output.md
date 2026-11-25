## REFORMULACION
Encargo ejecutable (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1`. Propósito: permitir lectura pública de un store sin migrarlo ni escribir en disco, observar cambios de otros procesos y rechazar de forma observable un store no preparado; además, extraer payload de texto ya leído. Resultado: `sldb.api` exporta `read_store`, `store_is_prepared` y `extract_payload`, con tests, CHANGELOG y nota en `docs/architecture/`. Límites: no cambiar `open_store` ni `mode="readonly"`, no tocar `graph_ui`, no servirlo por `sldb serve`.

## AMBIGUEDADES
1. «los cuatro comandos de Validation pasan» frente a tres comandos listados en Validation. Obliga a inventar cuál es el cuarto.
2. «read_store(store: str | Path | None = None) que resuelve el store igual que open_store (_resolve_store_arg o _find_default_store("readonly"))». No fija precedencia ni comportamiento exacto con `None`; obliga a inventar la resolución.
3. «se mueve o reexporta desde src/sldb/store/migration.py sin cambiar su lógica». Obliga a elegir entre mover y reexportar, y dónde queda `_already_canonical`.
4. «llama add_owner_import_roots, new_operation y new_documents_hash_operation y devuelve StoreLocation». No especifica orden, imports ni construcción de `StoreLocation`; obliga a inventarlos.
5. «read_store nunca escribe en disco» y «audit hook o comparación de mtimes». No define qué cuenta como escritura; obliga a inventar el criterio del test.
6. «extract_payload(model, markdown) -> dict» y «devuelve lo mismo que extract_model_data». No fija tipos ni mapeo de argumentos; obliga a inventarlos.
7. «fixture de tests/store/test_legacy_layout_migration.py». No nombra la fixture ni si es reutilizable; obliga a inventar extracción o duplicación.
8. «una línea en docs/architecture/». No indica archivo; obliga a elegir uno.

## DRY-RUN
No ejecutado. Lecturas previstas: `open_store.py`, `migration.py` (49-75), `api/__init__.py`, fixture legacy, `extract_model_data`, tests API y `tools/check.sh`. Cambios previstos: crear `read_store.py` y `extract_payload.py`; ajustar `migration.py`; exportar en `api/__init__.py` y `__all__`; añadir tests; actualizar CHANGELOG y docs. Dependencias: resolución de store, comprobación canónica, operaciones de runtime, validación runtime, fixtures y capas de `check.sh`. Validaciones futuras: los tres pytest/check listados y el `python -c` de Done When. Es tarea ejecutable, no agregado.

## FUTURO
Otro nodo ejecutor implementará y correrá las validaciones. El cierre operativo —commit y mensaje a `graph_ui`— y la adopción de la API por `graph_ui` corresponden a otro nodo o a un humano.
