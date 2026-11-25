## REFORMULACION

Encargo: en el repo sldb, hacer que `docs track --force` (y `track_document_file(..., force=True)`) sobre un documento ya trackeado con igual modelo, nombre y ruta lo re-indexe desde el archivo actual —shard, índice y aristas— sin duplicar la declaración; con force y ruta distinta debe fallar con `SLDBStoreError` nombrando ambas rutas; sin force no cambia nada. Incluye docstring/ayuda, tests en `tests/api/test_api_documents.py`, `CHANGELOG.md` y verificar `make world` de pron. Superficie: `src/sldb/store/ops.py`, `src/sldb/api/documents/track_document_file.py`. Límites: no tocar pron ni su CI. El nodo es un TaskDoc: no ejecutable; se cumple mediante la implementación descrita.

## AMBIGUEDADES

1. "re-indexa ese documento desde el archivo como lo haría una edición externa reconocida": no se identifica qué camino concreto es; obliga a inventar el punto de reutilización.
2. "shard, índice y aristas al día": no aclara si las aristas se recalculan ni con qué alcance; obliga a inventar la semántica.
3. "mismo modelo, nombre y ruta": no define igualdad de ruta (normalización, symlinks); obliga a inventar el criterio.
4. "Hoy force solo salta la comprobación de round-trip": no dice si el nuevo force conserva ese salto; obliga a inventar la combinación.
5. "declare_tracked queda idempotente": no concreta si implica no reescribir o solo no duplicar; obliga a inventar.
6. "falla con SLDBStoreError que nombra las dos rutas": no fija mensaje ni formato; obliga a inventar texto y orden.
7. "check_store ok": no define comando ni API; obliga a inventar la comprobación.
8. "clonar pron (master) a /dev/shm": no da URL/origen ni red disponible; obliga a inventar el clonado.
9. "result-summary.md": no indica ubicación; obliga a inventar la ruta.
10. "aviso a sldb-ui y a pron": no fija canal ni formato; obliga a inventar la notificación.

## DRY-RUN

Lecturas: `ops.py` (`track`, `_pre_check`, `_do_track`), `track_document_file.py`, `declare_tracked` y el camino de reindexado por edición externa; tests existentes y CHANGELOG. Cambios previstos: propagar `force` a `StoreOperations.track`; con force y misma ruta reindexar bajo `store_lock` sin duplicar declaración; con ruta distinta lanzar `SLDBStoreError` con ambas rutas; actualizar docstring/ayuda; añadir cuatro tests; CHANGELOG. Dependencias: `store_lock`, `declare_tracked`, helpers de reindexado, clon de pron y venv editable (red). Validaciones futuras: los seis `pytest` y `check.sh --fast`; `make world` de pron con rc 0; revisión de `result-summary.md`. Nada se ejecuta aquí.

## FUTURO

Deciden otros nodos o humanos: qué camino de reindexado reutilizar, el criterio de normalización de rutas, si force mantiene el salto de round-trip, el formato del error y de la idempotencia, la ubicación de `result-summary.md`, el canal de aviso y la aprobación del commit. El nodo de implementación produce diff y evidencias; el revisor humano valida.
