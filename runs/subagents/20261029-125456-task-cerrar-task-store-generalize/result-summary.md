# Result: verify TASK-store-generalize (no code changes)

Task: task-cerrar-task-store-generalize-storecodec-y-storeerror-ya-existen
Mode: shared-plain, `/workspace/sldb`, branch main. Verification only. No code or desk/ edits, no closeout.
`TASK-store-generalize.md` is NOT deleted (the supervisor does the `git rm` at closeout).

## Requirement -> file -> evidence

| Requirement (TASK text) | File | Evidence |
|---|---|---|
| Store has `StoreCodec` Protocol | `src/sldb/store/codec.py:7-10` | `@runtime_checkable class StoreCodec(Protocol): def extract(self, model_type: Any, markdown_text: str) -> dict[str, Any]` |
| Real default codec `RuntimeCodec`, with a LOCAL import of `extract_model_data` | `src/sldb/store/runtime_codec.py:7-11` | `class RuntimeCodec` / `from sldb.runtime.validation import extract_model_data` is inside `extract()` (indented, line 10) |
| `default_codec: StoreCodec = RuntimeCodec()` | `src/sldb/store/codec.py:14` | literal line. Runtime check: `isinstance(default_codec, StoreCodec) == True` |
| Coupling 2: `extract_model_data` gone from `hashing`/`query`/`semantic` | `hashing.py:5,20,41,51`; `query.py:5,22,29,52,64`; `semantic_doc_contribution.py:13,20`; `semantic_doc_tags.py:15,21,32`; `edge_rebuild.py:13,67` | `grep -rnE 'StructuredNLDoc\|extract_model_data' src/sldb/store` finds `extract_model_data` ONLY in `runtime_codec.py:8,10,11`. The others import `from sldb.store.codec import StoreCodec, default_codec` and take `codec: StoreCodec = default_codec` (`hash_fields`, `hash_field_map`, `_load_doc`, `_load_one`, `load_runtime_documents`, `process_doc`, `tags_of`). |
| Coupling 1: `StructuredNLDoc` gone from `diagnostics`/`hashing` | `diagnostics.py`, `hashing.py` | grep finds `StructuredNLDoc` only at `model_contract.py:20,22` (local import in a function body, indented) and in a docstring (`semantic_tags.py:7`). No top-level import. |
| Coupling 3: `sldb.core.exceptions` not imported at module top level by `facade`/`ops`/`io/*` | `facade.py:11`, `ops.py:35`, `io/lock.py:50` | These are local, function-body imports: `from sldb.store.exceptions import SLDBError` / `SLDBStoreError`. No other file in `store/` matches `sldb\.core`, except the seam below. |
| `StoreError` exists | `src/sldb/core/exceptions/store_error.py` (see deviation 1) | `class StoreError(Exception)`. Re-exported at `src/sldb/store/exceptions.py:9`. |
| `SLDBStoreError` also subclasses `StoreError` | `src/sldb/core/exceptions/sldb_store_error.py` | `class SLDBStoreError(SLDBError, StoreError)`. Runtime check: `issubclass(SLDBStoreError, store.exceptions.StoreError) == True`. CLI `except SLDBStoreError` still matches (same class). |
| No top-level runtime/core/structured_doc imports in the store, except the declared seams | `tests/test_store_seams.py` (2 tests) | `test_only_the_seams_import_the_core_the_models_or_the_runtime`, `test_nothing_in_the_store_imports_the_layers_above_it`: 2 passed. The seams are `exceptions.py`, `runtime_codec.py`, `model_contract.py`. |

Top-level (column 0) imports of `sldb.*` outside `sldb.store`, found by grep over `src/sldb/store`; this is the full list:
```
model_contract.py:15  from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_payload  # plain data
exceptions.py:8       from sldb.core.exceptions import SLDBError, SLDBGraphCycleError, SLDBModelError, SLDBStoreError
exceptions.py:9       from sldb.core.exceptions.store_error import StoreError
runtime_codec.py:4    from sldb.models.provenance_block import index_block
```
All four are in the three declared seam files. `runtime.validation`, `structured_doc` and `core.exceptions` are imported at top level only by `store/exceptions.py`.

## Validation

Command, run from `/workspace/sldb`:
```
PYTHONPATH=/workspace/sldb/.venv/lib/python3.13/site-packages \
  /home/scion/.local/share/uv/tools/structuredlanguagedb/bin/python -m pytest -q tests -k 'codec or exceptions or store'
```
Exit code: **0**. Result: `650 passed, 965 deselected, 2 warnings in 91.10s`. Log: `validation.log` in this directory.

Extra: `... -m pytest -q tests/test_store_seams.py` gave exit 0, 2 passed.
Import check: the interpreter loads `sldb.store.codec` from `/workspace/sldb/src` (pyproject has `pythonpath = ["src", "."]`).

## Deviations from the TASK text (old iso-lab worktree request)

1. **`StoreError` lives in the core, not in `store/exceptions.py`.** TASK Part C.1 defined it in `src/sldb/store/exceptions.py`. Actual: it is defined in `src/sldb/core/exceptions/store_error.py`. Its docstring says the core must be able to name it without importing the persistence layer (importing it from the store pulled 46 extra modules into every core import). `sldb_store_error.py` imports it from `.store_error`, not from `sldb.store.exceptions`. `store/exceptions.py` re-exports it.
2. **`store/exceptions.py` is not just a `StoreError` class.** It is the store's one error seam: it re-exports `SLDBError`, `SLDBGraphCycleError`, `SLDBModelError`, `SLDBStoreError` and `StoreError` from `sldb.core.exceptions`, with a TOP-LEVEL import of `sldb.core.exceptions`. The TASK expected zero top-level `sldb.core.exceptions` imports. Instead the store's modules import errors from `sldb.store.exceptions`, and the seam test allows exactly that file.
3. **Store modules import `sldb.store.exceptions`, not `sldb.core.exceptions`.** Some do it at top level (`semantic_parents.py:13`, `semantic_doc_contribution.py:12`, `edge_rebuild.py:12`, `graph/analysis/order.py:7`, `graph/analysis/centrality.py:20`, `query_engine/where_parse.py:13`). `facade.py`, `ops.py` and `io/lock.py` use local imports as the TASK asked. Net effect: the coupling goes through one declared seam instead of local imports at each raise site.
4. **`RuntimeCodec` is in `store/runtime_codec.py`, not `codec.py`.** `codec.py` imports it from there and defines `default_codec`. The local import of `extract_model_data` is as specified. `runtime_codec.py` also has a top-level `from sldb.models.provenance_block import index_block` (the seam for a document's provenance block), which the TASK did not mention.
5. **Codec threading goes beyond the TASK's three files.** Also covered: `semantic_doc_contribution.py`, `semantic_doc_tags.py`, `edge_rebuild.py`. `query.py` and `semantic_doc_tags.py` bypass the caches when `codec is not default_codec`.
6. **`model_contract.py` is a third seam.** It keeps `StructuredNLDoc` as a function-body import (line 20) and a top-level import of `sldb.models.builtin_relation_types` (plain data). Not in the TASK.
7. **Not run:** the TASK's `bin/lab-test.sh` baseline (sldb 411 / kgdb 23 / deskops 140) and the `git add -A && git commit` on `iso-lab/sldb`. The iso-lab worktree and Docker image are not available here, and the desk task defines the validation as the pytest command above. The counts are not comparable: this repo has 1615 tests, of which 650 were selected.
8. **The desk Done When wording says "a nivel de módulo ... ni core.exceptions".** Strictly, deviation 2 means `store/exceptions.py` does import `sldb.core.exceptions` at module level. The supervisor should decide whether the seam counts as satisfying it. The atom `atom-el-store-depende-del-resto-de-sldb-solo-por-costuras-y-un-test-lo-hace-cumplir` and `tests/test_store_seams.py` describe it as intended.

## Working tree notes for the supervisor

- No tracked files were changed by this run; the only addition is this directory (`runs/subagents/*-task-cerrar-task-store-generalize/`: `task.txt`, `validation.log`, `result-summary.md`).
- Pre-existing or other-agent changes were left untouched: `.deskops.log`, `.sldb/store.yaml` (new RunDoc entry for the sldb-serve run; task order swapped), `desk/tasks/task-cerrar-task-sldb-serve-*.md`, `desk/tasks/task-cerrar-task-store-generalize-*.md`, staged deletion `D TASK-sldb-serve.md`, untracked `.claude/`, `.herdr-coordination.md`, `runs/subagents/20261029-124912-task-cerrar-task-sldb-serve/`. The workspace is shared-plain, so another agent is working in the same checkout.
- To review: deviations 1, 2 and 8. Then `git rm TASK-store-generalize.md` and `deskops closeout commit`.
