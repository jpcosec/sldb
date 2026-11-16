# Resultado — executor deskops-e-98bf5ed2ff9f

Tarea: `task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio`
Pill aplicado: `pill-pill-dónde-se-agrupan-los-ausentes-de-sections-rebuild`.

## Cambios
- `src/sldb/store/semantic.py` (autorizado por el pill, sección How/Where): `RebuildReport.missing_paths: list[str]` nuevo.
- `src/sldb/store/section_sync.py`:
  - `_missing_doc(doc, d_path, root, report)`: ya no llama a `logger.warning`; suma `docs_skipped_missing`, agrega a `verbose` (como antes) y agrega la ruta relativa al proyecto (`os.path.relpath`, posix) a `report.missing_paths`.
  - `_sync_one_section`: pasa `root` a `_missing_doc`.
  - `process_model_sections`: guarda `len(report.missing_paths)` al entrar; tras `_sync_model_sections`, si hubo ausentes nuevos en esta llamada, emite un solo `logger.warning(missing_summary({m_entry.name: n}, rutas))`.
  - `missing_summary(per_model, paths)` nueva: `Sections rebuild: <n> documents missing on disk (<Modelo>: <n>[, ...]); e.g. <r1>, <r2>, <r3>`, modelos y rutas en orden alfabético, hasta 3 rutas.
- `tests/store/test_semantic_rebuild.py`: `test_missing_documents_log_one_summary_warning` — store en tmp_path con `api.init_store/add_model/create_document` (patrón de `tests/store/test_runtime_wiped.py`), 5 `Note` cuyos archivos se borran, cachés borradas, `rebuild_sections_indexes` con caplog: exactamente un warning, `"Sections rebuild: 5 documents missing on disk (Note: 5); e.g. notes/n0.md, notes/n1.md, notes/n2.md"`; además `docs_skipped_missing == 5`, 5 entradas en `verbose`, 5 `missing_paths`.
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet`.
- Llamadores (`payload_save_steps.py`, `untrack_document.py`, `rebuild_edges.py`) sin cambios.

## Done When
- Test nuevo pasa (5 ausentes → 1 warning que dice 5): sí.
- `tests/store/test_semantic_rebuild.py` completo pasa: 10 passed.
- CHANGELOG: sí. Commit: lo hace el coordinador (closeout); no hice commit ni push.

## Comandos
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py` → rc=0, 10 passed (salida en `validation.log`).

## Archivos tocados
- src/sldb/store/section_sync.py
- src/sldb/store/semantic.py
- tests/store/test_semantic_rebuild.py
- CHANGELOG.md
- runs/subagents/20261116-exec-sections-missing/{validation.log,result-summary.md}

## Desvíos y dudas
- **Una línea por modelo, no una por reconstrucción.** Las Precisiones dicen que emite "la función de nivel superior que arma el report"; esa es `rebuild_sections_indexes` en `src/sldb/store/section_rebuild.py`, que no está en los archivos del contrato. El pill dice que el aviso sale una vez por llamada a la función de section_sync que recorre los modelos y que, si se llama por modelo, una línea por modelo con ausentes es válido. `process_model_sections` se llama por modelo, así que manda el pill: una línea por modelo con ausentes (en el desk de sldb, una sola: todos son `PythonSymbolDoc`). El formato admite varios modelos (`missing_summary` recibe un dict) por si luego se mueve la emisión a `rebuild_sections_indexes`.
- `missing_summary` es pública (sin `_`) para poder reutilizarla desde `section_rebuild.py` si se hace ese cambio; no se usa fuera de section_sync hoy.
- Comprobación manual en el desk (paso 4, opcional según Precisiones): no hecha.
- `uv.lock` ya aparecía modificado antes (cambio ajeno); `uv run --frozen` no lo tocó por mi parte. No toqué los cambios ajenos.
- El test pasa `resolve_model_ref=None` a `rebuild_sections_indexes`: con todos los documentos ausentes nunca se resuelve el modelo.
