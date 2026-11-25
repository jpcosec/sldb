## REFORMULACION

Encargo: eliminar el ruido de miles de líneas “Sections rebuild: doc … missing” que imprime cada escritura en el desk cuando hay documentos generados ausentes. Resultado: en `src/sldb/store/section_sync.py`, acumular las rutas ausentes en `report.missing_paths`, dejar que `_missing_doc` solo agregue y emitir un único `logger.warning` al final de la reconstrucción, con el formato exacto indicado (n total, desglose por modelo alfabético, hasta 3 rutas alfabéticas). Añadir un test caplog en `tests/store/test_semantic_rebuild.py` (5 ausentes → 1 warning que dice 5) y una línea en `CHANGELOG.md` bajo “## 0.1.13 — not released yet”. Repo: SLDB_1. Límites: no cambiar los tres callers citados, no restringir la reconstrucción a los documentos de la transacción, no tocar cómo `stores check` reporta ausentes; el ejecutor no hace push; commit lo hace el coordinador.

## AMBIGUEDADES

1. “(<Modelo>: <n>[, <Modelo>: <n>...])”: no se define cómo obtener “Modelo” de cada ruta ausente (¿atributo del documento, prefijo del id, nombre de archivo?). Obligaría a inventar la derivación.
2. “agrega la ruta relativa al proyecto”: no se fija la raíz exacta de esa relatividad. Obligaría a elegir entre cwd, raíz del checkout u otra.
3. “la función de nivel superior que arma el report”: no se nombra la función ni se cubre el caso de llamadas anidadas o múltiples entradas. Obligaría a decidir dónde vive el emisor único.
4. “en un worktree limpio” frente a “una copia del repo en /dev/shm”: dos escenarios distintos para la comprobación manual. Obligaría a elegir uno.

## DRY-RUN

Lecturas: `section_sync.py` completo; `payload_save_steps.py:112`, `untrack_document.py:68`, `rebuild_edges.py:37` (solo confirmar que no cambian); `tests/store/test_semantic_rebuild.py` (fixtures/helpers); `CHANGELOG.md`; nota de inbox. Cambios previstos: campo nuevo en el report; `_missing_doc` sin warning; emisor final que agrupa, ordena y loguea una vez; test caplog; línea de changelog. Dependencias: helpers existentes o `sldb.api` en `tmp_path`; formato exacto del mensaje. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py`; comprobación manual opcional; verificar una sola línea y el conteo 5. Sin ejecutar nada.

## FUTURO

El ejecutor produce `runs/subagents/<run-dir>/result-summary.md`. El coordinador ejecuta `deskops closeout commit` y, si procede, `deskops message send --to <repo>`; el humano decide la comprobación manual y el push/merge.
