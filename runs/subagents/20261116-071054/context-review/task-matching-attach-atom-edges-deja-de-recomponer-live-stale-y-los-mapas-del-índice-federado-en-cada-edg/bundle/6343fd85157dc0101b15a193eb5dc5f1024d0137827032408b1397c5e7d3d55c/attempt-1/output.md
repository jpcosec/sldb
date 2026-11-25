## REFORMULACION

Encargo (nodo ejecutable, `task.debug`, repo sldb): hacer que `attach_atom_edges` cargue el índice de aristas una vez por store/llamada en lugar de recomponer live-stale y mapas por referencia, de modo que el `specir catalog build` de IR pase de >300 s a <60 s con idénticas aristas. Resultado: test contador en `tests/matching/` (≤2 `load_edge_index` para 10 referencias), cambio en `StoreReader` (`store_reader.py`), memoización solo si (2) no basta (`composed_reading.py`), medición antes/después en `runs/subagents/<run-dir>/result-summary.md`, línea de CHANGELOG y tres comandos pytest. Límites: no cambia semántica de stale, no toca `compose.py` salvo que (3) lo exija, no toca configuración de federación de IR; commit lo hace el coordinador, sin push.

## AMBIGUEDADES

1. "la ruta exacta se copia de la nota de origen (references)": la nota de inbox no está en el bundle. Obliga a inventar la ruta del `project.yml`.
2. "resuelva edges_from y edges_to de cada referencia sobre ese índice ya cargado": no consta API de `edge_reading` que lea sobre un índice cargado. Obliga a inventar función/firma.
3. "una sola vez por store" vs. "el test admite 2 porque edges_from y edges_to pueden necesitar el índice con y sin enlaces": ¿la meta es 1 por store o 2 (una por `include_linked`)? Contradicción operativa.
4. "compose_edge_index acierta la caché _COMPOSED": el código del bundle usa `load_composed`/`disk_key`, no `_COMPOSED`. Obliga a inventar/verificar nombre.
5. "shards_signature(store_path)": no consta en el bundle. Obliga a inventar su existencia/firma.
6. "el model_copy resultante reconstruye los mapas (_ensure_maps)": `with_live_stale` solo copia si hay `extra`. Obliga a inventar el diagnóstico exacto.

## DRY-RUN

Lecturas: los seis archivos nombrados, la nota de inbox (ausente), `tests/matching/test_matching_refs.py`, CHANGELOG. Cambios previstos: test contador con monkeypatch; reescritura de `StoreReader._read_edges`/`edges_of`; condicional memoización de `with_live_stale` con clave `(store_path, shards_signature, stat tuples)` en proceso. Dependencias: API de lectura sobre índice cargado, helpers de fixtures. Validaciones futuras: tres pytest con `TMPDIR=/dev/shm`, medición IR antes/después, commit del coordinador; aviso a repos.

## FUTURO

Decide el humano/IR si la medición cumple 60 s; el coordinador commitea y cierra con `deskops closeout`; el ejecutor solo escribe informe y avisos.
