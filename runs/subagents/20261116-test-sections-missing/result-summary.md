# Resultado — tester deskops-t-fcd90d896392

Tarea: `task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio`
Veredicto global: **PASA**

## Validation
| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py` | **PASA** — rc=0, `10 passed` (validation.log). `uv` funcionó; no hizo falta `uvx`. |

## Done When (por punto)
1. **Test nuevo pasa (5 ausentes → 1 warning que dice 5): PASA.** `test_missing_documents_log_one_summary_warning` corrido aislado con `-v`: 1 passed. Afirma exactamente `["Sections rebuild: 5 documents missing on disk (Note: 5); e.g. notes/n0.md, notes/n1.md, notes/n2.md"]`, `docs_skipped_missing == 5`, 5 entradas en `verbose`, 5 `missing_paths`.
   - **Prueba negativa propia:** el mismo archivo de test con `section_sync.py` de HEAD (copia de `src/` en /dev/shm vía `PYTHONPATH`) **falla**: salen 5 líneas `Sections rebuild: doc 'nX' missing at <ruta absoluta>`. El test discrimina el comportamiento viejo.
2. **test_semantic_rebuild.py completo pasa: PASA.** 10 passed, rc=0.
3. **CHANGELOG: PASA.** Una línea en español bajo `## 0.1.13 — not released yet`, primera de la lista, estilo de las vecinas (task, nota de inbox, qué cambió, test).
4. **Commit: no aplica al tester** (lo hace el coordinador con `deskops closeout commit`). Sin commit ni push del ejecutor: `git log` HEAD sigue en `26838382`.

## Scope / Precisiones
- `_missing_doc` ya no llama a `logger.warning`; agrega la ruta relativa al proyecto (posix) a `report.missing_paths`; `verbose` y `docs_skipped_missing` siguen como antes: **cumple**.
- Formato exacto, modelos y 3 primeras rutas en orden alfabético: **cumple** (verificado también con <3 rutas: `e.g. memos/m0.md, memos/m1.md`).
- Llamadores `payload_save_steps.py`, `untrack_document.py`, `rebuild_edges.py` y `section_rebuild.py`: **sin cambios** (`git diff HEAD` vacío).
- Emisión **una línea por modelo con ausentes**, no una por reconstrucción: desvío respecto de la letra de las Precisiones ("función de nivel superior que arma el report" = `rebuild_sections_indexes`, fuera de `files`), pero el pill lo declara explícitamente válido. Aceptado. En el desk de sldb (solo `PythonSymbolDoc` ausentes) da una línea.
- Sin texto viejo `missing at` en ningún log del paquete (grep en `src/` y en el script de bordes).

## Casos no cubiertos por el ejecutor (script `edge_cases.py`, corrido desde /dev/shm, salida en validation.log) — 0 FAILS
- Store sin ausentes → ningún warning de Sections.
- Dos modelos con ausentes (Note: 4, Memo: 2) en un rebuild en frío → exactamente 2 líneas, cada una con su número y modelo; Note con 3 ejemplos alfabéticos de 4; Memo con 2 ejemplos; `docs_skipped_missing == 6`.
- **Escritura real por la API** (`api.create_document` con ausentes en el store, pasa por `payload_save_steps`) → 2 líneas resumen (una por modelo), ninguna por documento.
- Rebuild con caché caliente → solo vuelve a avisar el modelo cuyo índice no está cacheado (Memo); no es regresión.

## Archivos fuera del contrato
- `src/sldb/store/semantic.py` (+1 línea, `RebuildReport.missing_paths`): fuera de `files`, pero autorizado por el pill (Where/How). Aceptado; el coordinador debe incluirlo en el closeout.
- `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml`, `.sldb/core/documents/RunDoc/run-deskops-{e-98bf5ed2ff9f,t-fcd90d896392}.yaml`: registro de los RunDoc de este despacho (exec/test), no del ejecutor.
- `uv.lock`, `apply_batch.py`, `io/lock.py`, `tests/api/test_apply_batch_lock.py`, `desk/runtimes/`, `.herdr-coordination.md`: cambios ajenos listados; no tocados ni revisados. `runs/subagents/20261115-*` y `20261116-0*` (carpetas `context-review`) no están en la lista de ajenos del brief pero son de otras corridas, no del ejecutor.
- Paso 4 opcional (comprobación manual en el desk): no hecha por el ejecutor ni por mí; cubierta en parte por el caso de escritura real por la API.

## Archivos del tester
- runs/subagents/20261116-test-sections-missing/{validation.log,result-summary.md,edge_cases.py}
