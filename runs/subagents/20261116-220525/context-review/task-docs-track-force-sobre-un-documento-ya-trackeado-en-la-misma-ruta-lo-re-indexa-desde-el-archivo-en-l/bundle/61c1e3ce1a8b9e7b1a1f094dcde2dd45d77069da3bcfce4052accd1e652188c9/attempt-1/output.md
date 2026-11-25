REFORMULACION

Propósito: en sldb, hacer que `track_document_file(..., force=True)` y `docs track --force` re-indexen un documento ya trackeado en la misma ruta (shard, índice y aristas) en lugar de fallar con "already tracked"; sin force nada cambia; con force y ruta distinta, `SLDBStoreError` que nombre ambas rutas. Resultado: tests nuevos en `tests/api/test_api_documents.py`, docstrings/ayuda, CHANGELOG y `make world` de pron en verde contra este sldb. Repo: sldb, con `src/sldb/store/ops.py` y `src/sldb/api/documents/track_document_file.py` como superficie. Límites: no tocar pron ni su CI.

AMBIGUEDADES

1. "re-indexa ese documento desde el archivo como lo haría una edición externa reconocida": no nombra la función concreta; obliga a inventar si se reutiliza update/sync y con qué validaciones.
2. "declare_tracked queda idempotente": el input no muestra su implementación; obliga a inventar si ya lo es o hay que modificarla.
3. "con force... re-indexa" no aclara si se saltan round-trip, ruido estructural y frontmatter (hoy `force` los salta); obliga a decidir si un archivo inválido se re-indexa o se rechaza.
4. "anotar el resultado en result-summary.md": no se indica ruta; obliga a inventarla.
5. "aviso a sldb-ui y a pron": canal no especificado; obliga a inventarlo.

DRY-RUN

Lecturas: `ops.py` (`track`, `_pre_check`, `_do_track`), `track_document_file.py`, `declaration_sync.declare_tracked`, el camino de edición externa/sync, tests y conftest. Cambios previstos: propagar `force` por `StoreOperations.track` hasta `_do_track`; con force y misma ruta re-indexar por el camino de edición externa sin duplicar la declaración; con ruta distinta, error con ambas rutas; docstrings/ayuda; cuatro tests; CHANGELOG. Dependencias: idempotencia de `declare_tracked`, `store_lock`, hashes/aristas. Validaciones futuras: los seis comandos del TaskDoc y `make world` de pron en clon limpio. Sin ejecutar nada.

FUTURO

Un nodo ejecutor implementa y corre las validaciones; un humano decide el canal de aviso y aprueba el cierre; otro nodo/CI reproduce `make world` de pron.
