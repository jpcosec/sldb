## REFORMULACION

Encargo: en el repo `sldb` (cwd `/mnt/ssd/proyectos/SLDB_1`), corregir `sldb.api.read_store` para que distinga dos fallos que hoy comparten mensaje. Resultado: lanza `SLDBStoreError` con `store not found: <ruta>` cuando no existe el directorio del store, y conserva `store not prepared: run \`sldb stores update\` (<ruta>)` cuando existe pero falta el índice. Toca `src/sldb/api/stores/read_store.py`, `tests/api/test_api_stores.py` y `CHANGELOG.md`. Límite: solo esos dos mensajes; no cambiar otros. Es una tarea ejecutable única (no agregado): su validación son los tres comandos listados.

## AMBIGUEDADES

1. «y en `store_is_prepared` si hace falta» — no fija criterio; obligaría a inventar si se modifica el predicado o se añade una comprobación previa en `read_store`.
2. «cuando no existe el directorio del store» — no aclara si la ruta es el `.sldb` o el proyecto; obligaría a inventar el predicado (`store_exists` vs `Path.exists`).
3. «`store not found: <ruta>`» — no fija si `<ruta>` es la entrada sin resolver o la resuelta (el mensaje actual añade `({store_path})`); obligaría a inventar el formato exacto.
4. «tests ... para los dos mensajes» — no dice si ampliar el test existente de store sin preparar o añadir uno nuevo; obligaría a inventar la estructura de tests.
5. «aviso a graph_ui» — sin canal ni formato; obligaría a inventar el mecanismo de notificación.

## DRY-RUN

Lecturas: `read_store.py`, `store_discovery._resolve_store_arg`, `store/layout` (`store_exists`, `store_index_path`), `tests/api/test_api_stores.py` y el test de store legacy. Cambios previstos: comprobación de existencia antes de `store_is_prepared` en `read_store`, nuevo mensaje; test del caso inexistente y conservación del de no preparado; entrada en CHANGELOG. Dependencias: semántica de `store_exists` y comportamiento de `_resolve_store_arg` para alias. Validaciones futuras: los tres comandos del TaskDoc, ejecutados por el nodo de testing; luego closeout con commit atómico.

## FUTURO

`graph_ui` recibe el aviso y ajusta su respuesta 503; un humano decide el commit y ejecuta `deskops closeout`; los rituales de testing, closeout y fase consumen el resultado. No es ambigüedad del encargo.
