## REFORMULACION

Nodo ejecutable (`task.debug`) en el repo SLDB_1/sldb. Propósito: eliminar el coste por referencia de `attach_atom_edges` durante `specir catalog build` de IR, donde `edges_of` recompone live-stale y mapas del índice federado. Resultado: cargar el índice de aristas una vez por store y resolver `edges_from`/`edges_to` sobre él; el build de IR debe bajar de >300 s a <60 s con el mismo resultado. Incluye test contador, cambio en `StoreReader`, memoización condicional de `with_live_stale`, medición antes/después, CHANGELOG y commit. Límites: no cambia la semántica de stale, no toca `compose.py` salvo que exija la memoización, no modifica la federación del store de IR.

## AMBIGUEDADES

1. “carga el índice de aristas una sola vez por store” frente a “load_edge_index a lo sumo 2 veces para 10 referencias”: obliga a inventar si dos cargas son aceptables y por qué.
2. “memoizar with_live_stale … por firma de shards y stats de fuentes”: no define la firma ni la invalidación; obliga a inventar clave de caché.
3. “con el mismo resultado”: no fija criterio de equivalencia; obliga a inventar comparación de salida.
4. “el comando de IR de la nota”: no está transcrito ni la ruta del repo IR; obliga a inventar comando y ubicación.
5. “un store de prueba”: no identifica fixture; obliga a inventar su construcción.

## DRY-RUN

Un ejecutor leería los archivos listados, los tests existentes y la nota de inbox. Añadiría un test con contador sobre `load_edge_index` para 10 referencias. Modificaría `StoreReader` para cargar el índice una vez y consultar `edges_from`/`edges_to` sobre él. Solo si la medición no alcanza, memoizaría `with_live_stale`. Actualizaría CHANGELOG. Dependencias: APIs de edge index, fixtures de matching y comando/ruta de IR. Validaría con los tres pytest indicados, el test contador, medición antes/después y commit. Sin ejecutar nada.

## FUTURO

El ejecutor decide, tras medir, si aplica la memoización del paso (3) y documenta la medición. Un revisor humano valida el umbral <60 s y la equivalencia funcional. La configuración federada de IR queda fuera y la decide su responsable.
