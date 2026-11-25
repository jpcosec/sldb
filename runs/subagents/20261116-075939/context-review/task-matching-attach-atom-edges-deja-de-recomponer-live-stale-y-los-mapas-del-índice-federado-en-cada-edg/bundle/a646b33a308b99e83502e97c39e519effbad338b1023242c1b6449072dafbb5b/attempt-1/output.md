## REFORMULACION

**Propósito:** que `attach_atom_edges` deje de recomponer live-stale y los mapas del índice federado en cada `edges_of`, cargando el índice una vez por store y llamada. **Resultado:** test contador que exige ≤2 `load_edge_index` para 10 referencias, mismo conjunto de aristas, y `catalog build` de IR bajo 60 s medido antes/después. **Repo:** sldb en SLDB_1, con medición en `/mnt/ssd/proyectos/SLDB_1/IR`. **Límites:** no cambia la semántica de stale, no toca `compose.py` salvo que el paso (3) lo exija, no altera la federación del store de IR; CHANGELOG bajo "## 0.1.13 — not released yet"; el ejecutor no hace push.

## AMBIGUEDADES

1. "la ruta exacta se copia de la nota de origen (references)" — la nota no está en el input; obligaría a inventar la ruta del `project.yml` del comando de IR.
2. "para 10 referencias sobre un store de prueba" — `matching_store` (test nombrado) solo tiene dos documentos; obligaría a inventar ocho referencias o duplicarlas.
3. "carga el índice de aristas una sola vez por store" (Goal) frente a "el test admite 2" (Precisiones) — obligaría a decidir cuál es el criterio exacto de aceptación.
4. "Medición antes y después" — no dice cómo obtener el "antes" una vez modificado el árbol (stash, worktree, commit); obligaría a inventar el procedimiento.

## DRY-RUN

**Lecturas:** `store_reader.py`, `store_edges.py`, `edge_reading.py`, `compose.py`, `composed_reading.py`, `edge_index.py`, `test_matching_refs.py`, su `conftest`, la nota origen vía `deskops message read`. **Cambios previstos:** test contador en `tests/matching/`; `StoreReader` guarda un `EdgeIndex` y resuelve `edges_from`/`edges_to` por referencia; solo si no basta, memoizar `with_live_stale` con clave `(store_path, shards_signature, mtime_ns/tamaño)`; línea en CHANGELOG. **Dependencias:** API de `EdgeIndex`, `shards_signature`, `disk_key`/`load_composed`. **Validaciones futuras:** el test contador, los tres `pytest`, y la medición del `catalog build` de IR con `timeout 300`.

## FUTURO

El coordinador ejecuta `deskops closeout commit` con el título corto de la tarea (sin push). El aviso a `<repo>` se envía con `deskops message send` o, si el repo no está registrado, queda como línea "Aviso a `<repo>`: ..." en `runs/subagents/<run-dir>/result-summary.md`. La aceptación de la medición y del cierre corresponde al humano/coordinador.
