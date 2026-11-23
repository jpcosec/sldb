# Resultado (intento 2)
Commit 6fb26545 en la rama deskops/deskops-e-3617fe0f6a32-a2. Archivo: tests/matching/test_matching_refs.py (solo el test; producción sin tocar, 9d09537c sigue siendo el arreglo).

## Cambio
El test contador parcheaba sldb.api.edges.edge_reading.load_edge_index, pero store_edges.py lo importa por nombre y el camino nuevo no pasaba por ahí (contador 0). Ahora parchea sldb.api.matching.store_edges.load_edge_index, exige 1 <= llamadas <= 2 y mantiene la comparación de aristas como conjuntos.

## Comprobación
- Con StoreReader real: pasa. Mutación (quitar la caché self._index): falla. Restaurado: pasa.
- tests/matching/: 33 passed.
- Medición de IR: la del intento 1 (>300 s antes, 54,9 s después, rc 0); no cambia, no se tocó producción.
- tools/check.sh --fast rc 1 por 'identidad' (workbench_demo sin clasificar), preexistente y ajeno a la tarea; el supervisor decide.
Aviso a IR: attach_atom_edges ya no recompone índice por referencia (commit 9d09537c).

Advance: bloqueado por el gate ritual-closeout (faltan recibos evidence de deskops closeout verify, los escribe el coordinador).
