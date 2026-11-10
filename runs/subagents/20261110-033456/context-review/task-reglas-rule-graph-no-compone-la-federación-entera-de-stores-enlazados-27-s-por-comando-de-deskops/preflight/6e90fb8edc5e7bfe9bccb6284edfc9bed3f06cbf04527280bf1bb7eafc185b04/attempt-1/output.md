## REFORMULACION

**Propósito:** eliminar la composición innecesaria de la federación entera de stores enlazados (~29 000 nodos, 27 s en frío) que `rule_graph` hace en cada evaluación de reglas, cuando las reglas del documento local podrían resolverse sin ella.

**Resultado:** `rule_graph` no compone la federación salvo que una regla lo necesite; los findings quedan idénticos; un comando de deskops vuelve a 1-2 s. Medido con `rule_graph` < 1 s y comando deskops < 2 s.

**Repo:** sldb (origin/main 37359542). Toca `src/sldb/api/rules/`, `src/sldb/store/edge_index/` si hace falta, `tests/api/` y `CHANGELOG.md`.

**Límites:** fuera la semántica del lenguaje de reglas, la transacción, el resto de `load_edge_index` para otros consumidores (salvo lo mínimo) y deskops (no se escribe en él).

## AMBIGUEDADES

1. "el cierre de los caminos de las reglas" (opción b): noción no definida; obligaría a inventar qué es el cierre de caminos.
2. "un camino que puede salir del store" (opción a): obligaría a inventar el análisis estático para determinarlo.
3. "invalidada por las firmas de los shards de cada store" (opción c): obligaría a inventar el esquema de firmas.
4. "deskops show task <una tarea> --root <copia>": obligaría a elegir qué tarea y ruta de copia.
5. "sobre copias de los stores de los 6 desks": rutas de las copias no indicadas; obligaría a inventarlas.
6. "salvo lo mínimo" en el alcance sobre `load_edge_index`: obligaría a decidir el umbral.

## DRY-RUN

**Lecturas:** `rule_graph.py:84`, `load_edge_index(True/False)`, `rules_on_write`, `rules_on_transition`, `rules check/explain`, tests de s4.

**Cambios previstos:** modificar `rule_graph` para elegir `load_edge_index(store, False)` cuando las reglas son locales (o vecinos, según diseño); posible ajuste en `edge_index/`; test de camino cruzado; CHANGELOG.

**Dependencias:** sldb main 37359542; copias en `/dev/shm` de los desks y de deskops; deskops main con PYTHONPATH a la rama.

**Validaciones futuras:** tabla de tiempos (s1), findings idénticos en 6 desks + test cruzado (s3), tests s4 de a uno, tests de deskops < 90 s.

## FUTURO

El diseño (a/b/c) lo elige y justifica el worker en su informe. Las precisiones son "decisión revisable" del coordinador del plan de deskops. La comparación de findings y tiempos la ejecuta quien tenga acceso a las copias de stores.
