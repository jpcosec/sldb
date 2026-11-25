## REFORMULACION
Propósito: que una reconstrucción de secciones con N documentos generados ausentes emita como máximo un `logger.warning` resumen (n, desglose por modelo y hasta 3 rutas) en vez de N líneas. Resultado: cambio en `src/sldb/store/section_sync.py` (acumular ausentes vía `report.missing_paths`, emitir al final con formato exacto), test con `caplog` en `tests/store/test_semantic_rebuild.py` (5 ausentes → 1 warning que dice 5) y línea en `CHANGELOG.md`. Repo: sldb. Límites: no cambiar llamadores (`payload_save_steps.py:112`, `untrack_document.py:68`, `rebuild_edges.py:37`), no limitar la reconstrucción a la transacción, no tocar `stores check`. Commit lo hace el coordinador con `deskops closeout commit`; el ejecutor no hace push.

## AMBIGUEDADES
1. "agrega la ruta relativa al proyecto a una lista nueva report.missing_paths": `RebuildReport` vive en `src/sldb/store/semantic.py`, que **no** figura en `files:`. Habría que inventar si se puede editar ese archivo.
2. "con modelos en orden alfabético": `_missing_doc` recibe `doc` y `d_path`; no se indica de dónde sale el nombre del modelo (`doc.model`, `m_entry.name`, otro). Obliga a inventar el atributo.
3. "la función de nivel superior que arma el report emite al terminar un solo logger.warning": no se aclara si es `process_model_sections` (uno por modelo → varios avisos con varios modelos) o un nivel superior (uno por store). Choca con "a lo sumo una línea".
4. "report.docs_skipped_missing y report.verbose en section_sync.py": no se dice si `verbose` deja de acumular una entrada por ausente o se mantiene. Obliga a decidir.
5. "un store de prueba con 5 documentos trackeados": el archivo de test actual no tiene fixtures de store; la convención remite a `sldb.api`, pero "trackeados" no define el verbo exacto (`add_model`/`create_document`).

## DRY-RUN
Lecturas: `section_sync.py` completo, `semantic.py` (dataclass), test y llamadores citados. Cambios previstos: campo nuevo en `RebuildReport`; `_missing_doc` deja de loguear y agrega ruta; emisión única al final; test con `caplog`; CHANGELOG. Dependencias: `pytest`, `caplog`, `sldb.api` en `tmp_path`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py`; el ritual de testing pediría además `stores check`/`tools/check.sh` por tocar el store.

## FUTURO
Coordinar: decidir si se permite editar `semantic.py`; aclarar nivel del aviso y origen del nombre de modelo. Humano/coordinador: `deskops closeout commit`, aviso a `<repo>` y comprobación manual opcional en copia `/dev/shm`; el ejecutor escribe `result-summary.md`.
