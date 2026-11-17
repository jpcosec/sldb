# Result: tester deskops-t-5a89500e7e0d

Tarea: task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse.
Executor: deskops-e-13131c57ccbe (cambio sin commitear). Pills: ninguno. Salida completa en `validation.log`; scripts de prueba (`inv.py`, `probe.py`, `probe2.py`) copiados en este directorio y ejecutados desde `/dev/shm/tact`. No edité el repo.

## Veredicto: PASA

## Validation (corrida propia, `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev ...`)
| Comando | Resultado |
|---|---|
| `pytest -q tests/api/test_provenance.py` | PASA: rc 0, 10 passed (incluye los 3 tests nuevos) |
| `pytest -q tests/api/test_anchors.py` | PASA: rc 0, 23 passed |
| `pytest -q tests/api/test_api_documents.py` | PASA: rc 0, 17 passed |
| `pytest -q tests/test_clean_code_rules.py` (también obligatorio por brief) | PASA: rc 0, 1206 passed |
| `bash tools/check.sh --fast` (también obligatorio por brief) | PASA: rc 0 |

No corrí la suite completa ni `sldb stores build --check`: Validation no los nombra y el brief los prohíbe (quedan para el integrador).

## Done When
- **Validation pasa con los tests nuevos**: PASA (tabla de arriba).
- **Ninguna función pública de escritura descarta actor**: PASA.
  - Inventario propio (`inv.py`, recorre con ast `src/sldb/api` buscando funciones sin `_` inicial con parámetro `actor`, posonly, args o kwonly, sync y async): 25 funciones. Coincide con el del ejecutor. Él además lista `SpecSync.__init__` y `StoreWriter.__init__`, que por la regla del `_` inicial quedan fuera; igual delegan en create/save/delete_document con `self.actor`.
  - Las que no leen `actor` (`track_document_file`, `untrack_document`, `add_model`, `inherit_model`, `reindex_model`, `remove_model`, `add_semantic_parent`, `remove_semantic_parent`, `add_semantic_equivalence`) dicen en su docstring "not recorded" o "no longer recorded". `delete_document` lo pasa a `untrack_document` y su docstring ahora dice que no se registra.
  - Diferencia menor con el informe del ejecutor: pone `create_model` entre las que "pasan actor hasta el sello", pero lo pasa a `add_model`, que no lo registra, y su docstring dice "no longer recorded". En realidad es una excepción documentada. No es falla.
  - **Prueba dinámica, con stores en `/dev/shm` (equivalente a tmp_path)**, cada función que dice firmar con `actor="x:<fn>"` deja `sldb.by == "x:<fn>"`: `create_document`, `save_document_payload`, `stamped`, `stamped_file`, `promote_model_draft(backfill=True)` (vía `apply_backfill`, via=`backfill_document`), `write_anchor` al crear (via=`create_document`), `write_anchor` al re-registrar (via=`save_document_payload`), `record_reconnection`, `sync_palette`, `sync_notation` y `save_projection_view`. `write_rendered_document` se cubre a través de `save_document_payload`. `sync_spec` no se probó por separado: comparte `StoreWriter` con `sync_notation`. En el store con notaciones también aparecen archivos con `by: agent`: son los `sldb/relation_types/*.md` que escribe `init_store` (via=`init_relations`), que no tiene parámetro `actor` y queda fuera del inventario.
  - **actor=None contra HEAD**: el mismo `probe.py` corrió sin actor contra el worktree y contra HEAD (`git archive HEAD` en `/dev/shm/tact/head`, con `PYTHONPATH` a su `src/`; se verificó con `sldb.__file__`). Las salidas son idénticas (`diff` → IGUALES): todo queda en `by: agent` con el mismo `via`. Las funciones de notaciones tienen por defecto `actor="sldb"`, que no cambió.
- **CHANGELOG**: PASA. Hay entrada en 0.1.13 y lo que afirma coincide con el diff. **Commit**: pendiente, porque el brief se lo prohíbe al ejecutor; va en el closeout.

## Casos que el ejecutor no cubrió (probados en /dev/shm)
1. Actor del proceso: con `set_actor("human:proc")` y `write_anchor(actor=None)`, el sello es `human:proc`. Un `actor="x:explicit_over_proc"` explícito gana sobre `set_actor`. Igual que en HEAD.
2. `SLDB_ACTOR=human:env` con `write_anchor(actor=None)` al crear deja `human:env`. Igual que en HEAD.
3. Mutación: si `record_reconnection` vuelve a llamar con `actor=None` escrito a mano, el inventario por ast la marca como `used=False` y su docstring no dice "not recorded", así que `test_no_public_write_function_drops_its_actor_without_saying_so` fallaría. El test atrapa la regresión del Rationale. Límite: el chequeo es sintáctico (le basta que se lea `actor`) y no detectaría un `actor` reenviado a una función que lo ignora. Eso lo cubren las pruebas dinámicas de arriba. Es solo una nota, no una falla.

## Alcance de archivos
- Del contrato: `src/sldb/api/anchors/anchor_docs.py`, `tests/api/test_provenance.py`, `CHANGELOG.md`.
- Fuera de `files`, aceptados por el coordinador: `src/sldb/api/semantic/dag_writes.py` y `src/sldb/api/documents/delete_document.py`. Comparé el AST de HEAD y del worktree con los docstrings vaciados y es idéntico en los dos archivos: **solo cambian docstrings**. PASA.
- Los demás cambios del árbol no son de esta tarea: `.sldb/` y `desk/` de la tarea del scan de enlaces, los RunDoc de los runs, `desk/runtimes/`, `.herdr-coordination.md` y `runs/subagents/*`. No los revisé ni los toqué. Los cambios ajenos que nombra el brief (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`) ya no aparecen como modificados en `git status`.

## Regresiones vecinas
Módulos de `src/` cambiados: `sldb.api.anchors.anchor_docs`, `sldb.api.documents.delete_document` y `sldb.api.semantic.dag_writes`. Los tests que los importan (`grep -rl`), además de los de Validation, se corrieron uno por uno y todos dan rc 0:
`tests/api/test_api_semantic.py` (8 passed), `tests/api/test_doc_anchors.py` (24), `tests/api/test_graph_source_parity.py` (13), `tests/api/test_rewrite_references.py` (21), `tests/api/test_tags.py` (36). Como no hubo fallas, no hizo falta comparar con HEAD.

## Entorno
`uv run --frozen --extra code --extra dev` funcionó sin errores. tree-sitter estaba disponible, así que los tests de anchors no se saltaron.
