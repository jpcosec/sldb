# Transactions: several writes undone together

`sldb.api.transaction(store)` opens a `Transaction` whose operations write at once and are undone
together when the block raises. `sldb.api.apply_batch(store, changes)` applies a list of changes
in one transaction after prevalidating them all, and `POST /save` delegates to it, which made
the batch route atomic (decision DA2). This is node GD24 of the plan
`generalizar-desde-deskops`: it absorbs the `DocTransaction` deskops kept in its own `doc_io`.

## The API

```python
from sldb import api

with api.transaction(store, pythonpath) as tx:
    tx.update("login", payload, expected_source_hash=entry.source_hash)
    tx.create("TicketDoc", "signup", payload)              # path: beside the model's documents
    tx.move("faq", "docs/faq.md")                           # same name, edges rebuilt
    tx.write_file("notes/outline.txt", data, expected_sha256=digest)
    tx.record("CHANGELOG.md")                               # the caller writes it; rollback restores it
```

| Operation | Delegates to | Guard |
|---|---|---|
| `create(model, name, payload, path=None)` | `create_document` | `path` must stay inside the project root; without it, the model's default directory (`transaction_paths.default_document_path`) |
| `update(ref, payload, expected_source_hash=None, expected=None)` | `save_document_payload` | `expected_source_hash` against `DocumentEntry.source_hash` first, then `expected` (the full payload) against the current one; the first that fails raises `ConflictError` |
| `delete(ref)` | `delete_document` | |
| `move(ref, new_path)` | `move_document` (new) | destination inside the root and free, else `SLDBStoreError` before anything moves |
| `track(path, model, name=None)` | `track_document_file` | name defaults to the file stem |
| `untrack(ref)` | `untrack_document` | |
| `write_file(path, bytes, expected_sha256=None)` | plain write | current bytes must hash to `expected_sha256` (None when the file is absent) |
| `record(path)` | nothing | snapshots a file the caller writes on its own |

`ref` is a document name or its path as the store records it; every path is relative to the
project root or absolute inside it. `ConflictError(SLDBStoreError)` carries `ref`, `expected`
and `actual`. Nothing of the write path was reimplemented: every operation calls the public
function it names, with its files snapshotted first.

## Semantics

- **Writes happen at once.** What one operation writes, the next one (and any reader in the
  process) sees: an `update` inside the transaction reads back with its new value. There is
  no deferred mode (GP2 stays out of this node).
- **Nesting joins.** A `transaction()` opened over a store that already has one open in the
  process joins it (one `TransactionState` per resolved store path, counted by depth). Only
  the outermost block rolls back: an inner block that ends well commits nothing on its own,
  and an outer block that then raises reverts the inner block's writes too. An inner block
  that raises defers to the outer one.
- **Rollback restores bytes, entries and shards.** Before each operation the transaction
  snapshots the bytes (or the absence) of every file that operation may move
  (`transaction_paths.document_files`): the document's Markdown, its entry shard under
  `.sldb/core/documents/<Model>/`, its semantic, sections and edges shards under
  `.sldb_cache/`, the model's index and edges shard, the store index, the store's own edges
  shard, the semantic DAG and the declaration `store.yaml`. The first snapshot of a path is
  the state the rollback goes back to, however many later operations touch it. This is
  `store/io/rollback.py`'s `rollback_on_error` spread over the whole transaction: it now
  exposes `snapshot` and `restore_all`, and the one-operation context manager is built on them.
- **A file moved without a snapshot is not silently left behind.** On entry the outermost
  transaction records the (mtime, size) signature of every file under `.sldb/` and
  `.sldb_cache/` (lock files aside). On rollback, a file that appeared without a snapshot is
  deleted; one that changed or disappeared without a snapshot cannot be restored and is reported.
- **Caches are forgotten after the restore** with the functions that already existed:
  `forget_store_caches(store, model)` for every model touched, `invalidate_index_cache()`,
  `invalidate_shard_cache()` and `invalidate_composed_edge_indexes()`. The runtime document
  cache keys on the files' signatures, so a restored file is re-read on its own.
- **A failure during the rollback is not swallowed.** `RollbackError(SLDBStoreError)` is
  raised chained to the original exception (`raise ... from original`), with `unrestored`: the
  paths still not as they were, relative to the project root, in the order their restore was
  tried. It lives in `sldb.store.io.rollback` and is re-exported by `sldb.api`.

## `apply_batch`

`apply_batch(store, changes, pythonpath=None) -> BatchReport` takes the same change dicts
`POST /save` takes: `id` (the document name, unique in the batch), `action` (`create`,
`update`, `move`, `delete`, `track`, `untrack`), and by action `model`, `payload`, `path`,
`expected_source_hash` and `expected`. It prevalidates every change before writing anything
(`batch_prevalidate`): shape, model registered, payload rendered and read back under the model
(G4), guards, document present or absent as the action needs, target path inside the project
and free. Then it applies them in one transaction: creates and tracks, then updates, then
moves, then untracks and deletes, request order within each group. `BatchReport.saved` lists
the ids in that order; a failure while applying rolls the whole batch back and re-raises.

## `POST /save` (contract change, DA2)

Request and successful response are unchanged (`{"ok": true, "saved": [...]}`), as are the
409 for a stale `expected` or a taken name or file and the 422 for a payload the model
rejects. What changed: a failure halfway through a batch no longer leaves the earlier changes
saved and reports `completed`; it is a 500 `{"ok": false, "error": ..., "rolled_back": true}`
with the store exactly as before. The route also accepts `expected_source_hash` as the guard
of an update, delete, move or untrack (a stale one is the same 409), and the actions `move`
(`path`), `track` (`model`, `path`) and `untrack`. `write_file` is not exposed over HTTP.
`cli/serve/save_plan.py` keeps the HTTP-shaped checks and their messages; the model checks are
`apply_batch`'s, mapped to 409 (`ConflictError`, `SLDBStoreError`) and 422 (`SLDBValidationError`).

## Every write path validates against the model (G4)

`sldb fields update`, `sldb docs update`, `POST /save`, `apply_batch` and `transaction` all
render the payload under the model and read it back before writing, so a `model_validator`
that rejects a value rejects it on every path, with the file, the entry and the indexes left
as they were. `tests/api/test_write_paths_validate.py` proves it with one test per path. No
route had to be fixed: the rendering itself instantiates the model.

## `replace_text` (GD27)

`sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None, pythonpath=None)`
replaces exactly `count` literal occurrences of `old` by `new` in a tracked document or in a
plain file under the project root, inside a transaction; `sldb docs replace REF --old OLD
--new NEW [--count N]` is its command (envelope `data` = what the function returns).

- `ref` is what `doc_status` resolves (`name`, `Model/name` or a tracked path); when it names
  no document it is a path relative to the project root, which must exist inside it. A path
  outside the root is `SLDBStoreError`; an absent one, or an ambiguous reference, is
  `SLDBDocumentTargetError`. A linked store's document is replaced from its own store.
- `old` is literal (no regex) and not empty; `count >= 1`. The count is `str.count` over the
  bytes decoded as UTF-8 as they are (no newline or Unicode normalisation): non-overlapping,
  left to right. Another number is `SLDBValidationError` naming it (`details: {seen,
  expected}`) and nothing is written.
- A tracked document: the replaced text is extracted and validated under its model
  (`model_validator` included) and the `on_write` rules run on that payload (`check_on_write`:
  the RuleDocs and the family `builtin:tag_namespace:*`, tags.md); any error leaves the file as
  it was (`SLDBValidationError`, `SLDBRuleViolationError`). Then, in the transaction, the
  document is untracked, its bytes rewritten (guarded by the sha256 that was read) and
  tracked again with the same model and name, so its entry and the derived indexes follow.
  The document extracts the same payload except the replaced text.
- A plain file: no model, no rule; `write_file` with the sha256 that was read.
- `transaction=None` opens its own `transaction(store)`; a `Transaction` given must be open
  over `store` and the writes join it (nested semantics above: the outermost block rolls back).
- Returns `{ref, path (relative to the root), tracked, model, name, count}`.

The retrack rewrites `store.yaml` as untrack and track do (`declaration_sync`): a path listed
under `include.paths` leaves its place and comes back at the end of its model's list.

## Out of this node

- An `on_write` rule (`RuleDoc`, GO08) raising inside a batch: GO08 was not closed when GD24
  was dispatched, so that part is not implemented nor tested here (TaskDoc q10).
- Deferred writes (GP2) and exposing `write_file` over HTTP.

## Measurement

Wall time of one `POST /save` with 20 updates on a 20-document store, served with
`build_handler` as `tests/test_serve.py` does (script outside the repo; "before" is the route
of commit `baacd852`, "after" this node), 2026-11-06 on a machine shared with other workers:

| | round 1 | round 2 | round 3 | pooled median (9 samples) |
|---|---|---|---|---|
| before (median of 3) | 1.861 s | 1.923 s | 1.943 s | 1.923 s |
| after (median of 3) | 2.203 s | 1.864 s | 3.914 s | 2.203 s |

The transaction adds, per update, the snapshot of the document's files (eleven small reads)
and, per batch, one signature walk of the store; the spread between runs (1.4 s to 4.6 s) is
the machine's, larger than that cost.
