## REFORMULACION
Encargo ejecutable (`task.code`, no agregado): en el repo `/mnt/ssd/proyectos/SLDB_1`, alinear tres textos que hoy mandan a reconstruir cuando un documento queda en `EdgeIndex.stale` por edición externa —descripción del campo en `edge_index.py:19`, docstring de `load_edge_index` en `edge_reading.py:17-18` y alerta `edges/stale` en `cli/commands/edges.py:73`— para que nombren `sldb stores update` (API `update_store_indexes`). Resultado: esos textos corregidos, un test nuevo en `tests/api/test_api_edges.py` que demuestre edición manual → aparece en `stale` → `rebuild_edges` no lo saca → `update_store_indexes` sí, entrada en `CHANGELOG.md`, commit y aviso a graph_ui. Límites: no cambiar el rehasheo de `rebuild_edges`, no tocar stale por documento en graph_ui; si el test muestra que `update_store_indexes` tampoco lo saca, detenerse y reportar.

## AMBIGUIDADES
1. "cambiar la descripción del campo stale... la docstring de load_edge_index" — no da el texto nuevo; obliga a inventar la redacción exacta.
2. "aviso a graph_ui con deskops message send --to graph_ui" — sin contenido del mensaje; obliga a inventarlo.
3. "CHANGELOG y commit" — sin texto de entrada ni mensaje de commit.
4. "grep -rn \"edges rebuild\" src/sldb docs/ para encontrar otros mensajes que manden a reconstruir por stale y alinearlos" — no define qué coincidencias son "por stale"; obliga a decidir el criterio.
5. "un store de prueba" — no identifica fixture ni helper; obliga a inventar el montaje.
6. Validación cita "tests/api/test_composition_edges.py", ausente de `files`.
7. "la tarea se detiene y el ejecutor reporta el caso" — sin canal ni formato de reporte.

## DRY-RUN
Lecturas: los cinco archivos de `files` más `src/sldb/api/edges/rebuild_edges.py` (citado en rationale). Cambios previstos: test primero, tres textos, posibles mensajes del grep, CHANGELOG. Dependencias: fixtures de store, `update_store_indexes`, `load_edge_index`, `rebuild_edges`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q` sobre ambos archivos de test; commit; mensaje a graph_ui. Nada se ejecuta aquí.

## FUTURO
graph_ui decide qué hacer con su bloqueo de grafo y el stale por documento; un humano revisa el reporte si el test falla y decide la continuación; otro nodo o revisor valida commit y CHANGELOG.
