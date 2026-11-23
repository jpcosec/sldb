# Resultado
Commit en la rama deskops/deskops-e-3617fe0f6a32 (worktree .worktrees/deskops-e-3617fe0f6a32).
Archivos: src/sldb/api/matching/store_reader.py, src/sldb/api/matching/store_edges.py (edges_of_index, load_index), tests/matching/test_matching_refs.py, CHANGELOG.md.

## Cambio
StoreReader carga el índice con enlaces una vez por store (y los títulos) y resuelve edges_from/edges_to de cada ref sobre él, en vez de llamar edges_of (2 load_edge_index por ref). No se tocó composed_reading.py: el paso (3) no hizo falta.

## Test
test_attach_atom_edges_loads_the_edge_index_at_most_twice_for_ten_refs: antes 20 llamadas (falla), ahora <=2; compara como conjuntos las aristas con las de store_edges.edges_of.

## Medición (specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml, venv /tmp/ir-venv, IR rev del checkout)
- Antes: timeout 300 s, rc 124 (dos intentos; cProfile: 225 s en edges_of, compose 10 veces).
- Después: 54,9 s, rc 0 (48 s de CPU). La corrida es en frío para el proceso; la caché de disco `.sldb_cache` pudo estar parcialmente caliente por las corridas previas. Margen bajo 60 s estrecho: el grueso restante es la primera composición (lectura YAML de shards).
- Nota: PYTHONPATH del entorno apunta al sldb del checkout principal; se sobrescribió con el src del worktree para medir.
- No comparé byte a byte before/after.html (el before no terminó).

## Validación
Ver validation.log: tests/matching 33 passed; test_api_edges 17 passed; test_live_stale_security 8 passed.
**tools/check.sh --fast sale rc 1**: FAIL «identidad» por `workbench_demo` (directorio versionado sin clasificar, commit 562847e2), preexistente y ajeno a la tarea. Commiteé igualmente; el supervisor decide.
Aviso a IR: attach_atom_edges ya no recompone índice por referencia; catalog build de ejemplo ~55 s (commit en la rama del worktree).
