# result-summary H11b
run_id: run-deskops-e-417ece12b2b1
session: scion://agent/deskops-e-417ece12b2b1
session_sha256: (sin archivo de sesion)

## Hecho
- b2: `src/sldb/store/query_engine/document_rows_disk.py` (nuevo) + `document_selection.candidates`: caché JSON `.sldb_cache/document_rows/<id>.json` del store que llama; clave solo de stats (índice del store, stat y roster_hash de cada models index, dirs de shards de documentos, versión del índice, formato). Cualquier diferencia/corrupción = fallo, se lee como antes.
- b3: `networkx` perezoso (`store/graph/analysis/lazy_networkx.py`, usado por 6 módulos de analysis y `store/semantic_dag_graph.py`): sldb.api 0,539 -> 0,454 s de import (>0,1 s en el CLI). `load_declaration` lee con CSafeLoader (fuera de la lista de archivos: store_declaration.py; mismo dato que safe_load).
- b4: `tests/api/test_select_documents_disk.py` (6 tests: mismo resultado y revisión con/sin caché, documento trackeado invalida, caché corrupta/otra versión ignorada).
- b5: docs/architecture/views.md, CHANGELOG.md. contracts/layers.toml: persistencia needs 24->25, grafo needed_by 8->9 (medidos por check.sh).

## Mediciones (layout H11 reconstruido por git archive en /dev/shm/h11b, deskops ef84b70d; bench en bench-run-board.sh)
- sldb views run board, store construido, proceso nuevo, mediana de 5: base 2,16 s -> 1,44 s.
- primera corrida tras build (sin cachés): 6,7 s -> 6,5 s.
- Meta <1 s NO alcanzada: faltan ~0,45 s. Restante: import de modelos pydantic ~0,45 s, JSON del índice compuesto ~0,13 s, live_stale (1325 docs) ~0,3 s bajo perfil, resto de la vista. Eso es del índice compuesto (H11, fuera de alcance) y de deskops.
- Nota: el layout no usa worktrees de los repos hermanos (no toqué su .git); la base absoluta difiere de los 1,59 s de H11 (otra carga/layout).
- Perfiles: importtime-before/after.txt, cprofile-before/after-b2.txt.

## Revisar
- Límite conocido: edición in situ de un shard sin rename y sin mover roster_hash no se detecta (igual que H11).
- Archivos commiteados: ver lista del commit.
