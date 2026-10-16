# Changelog

Version note (2026-09-13, updated 2026-10-16): `pyproject.toml` declares `0.1.2`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.4 - 2026-10-16 — `fields update` leaves the store passing

- A field write (`fields update|append`, `sldb.api.save_document_payload`) rewrote the Markdown
  and the model's roster but not the document's record, so `stores check` failed with a
  `data_mutation` on the write sldb had just made. The shard cache handed out its own instance:
  the caller edited it in place and the save, comparing against the cache, saw no change and
  skipped the write. Loads now return a copy (`sldb.store.io.shards`), which also covers the
  semantic, sections and edges shards.

## 0.1.3 - 2026-10-16 — upgrading sldb no longer fails unchanged stores

Found on Governance's `pulse`, which installs sldb from git: both checks failed on a store whose
content had not changed.

- `stores check`: a model whose stored contract hash equals the formula sldb used before
  cecd97b (fields and template only) passes, with a note naming those models, instead of
  "contract moved" on every model. A class that really changed still fails. `stores update`
  re-seals the hash under the current formula. JSON: `models[].legacy_contract`.
- `edges check`: in a store that ran `edges init`, an edge sldb derives itself whose builtin
  type was added later (`composes`) is checked against the definition sldb ships and reported in
  `untracked_builtins`, not as an error. A store that never ran `edges init` still fails;
  authored edges still need a tracked type.

## 0.1.2 - 2026-10-16 — referencing documents of linked stores

- `stores add` links were recorded but no document lookup read them: `docs show
  alias:doc` answered `Unknown document target`. `docs show` (and `sections show|fields`,
  serve's document routes) now take `alias:ref` — name, `Model/name` or tracked path — and
  read only the store linked directly as `alias`. A bare ref still reads only the local store;
  a prefix that names no link leaves the ref whole, so existing refs resolve as before.
- Add `docs exists <[alias:]ref>` and `sldb.api.doc_status|doc_exists`: whether a reference
  resolves, from the indexes alone (no model import, nothing written). Exit 0 ok, 1 missing,
  2 ambiguous, 5 `link-missing` / `link-broken`, so a missing document is told apart from a
  sibling repo that is not there.
- `stores list` (and `sldb.api.store_links`) report each link's state: `ok`, `missing` or
  `not-a-store`; a broken link is reported, never raised.
- `stores add` records the link relative to the project root (it was absolute outside it), and
  refuses linking a store to itself, aliases outside `[A-Za-z0-9][A-Za-z0-9._-]*` and the
  reserved `local`. Links already written are read as before.
- `stores init` seals the root hash over the empty model layer: a new store, or one that
  only links others, passes `stores check` without a `stores update`.
- `docs show` of a linked doc reads its file from the linked project (`absolute_path` was
  built from the local root).

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

## Working tree — `docs delete`

- Add `docs delete` (and `sldb.api.delete_document`): untrack a document **and** remove
  its Markdown file. `docs untrack` was the only way to drop a document, and it keeps
  the file on purpose — so "delete this document" meant untrack, then `rm` by hand, then
  remember that `runtime/cache/extracted.json` still describes the deleted path until
  some later full load rewrites it. `delete` does the three.
- Confirms before removing the file unless `--yes` is given; a non-interactive stdin
  answers no.
- Add `runtime_cache_disk.forget(store, predicate)` so cache entries can be dropped
  without a full store load.

## Working tree — self-documentation follow-up

- Add `selfdoc scan|sync|check` to derive CLI facts from argparse, preserve authored explanations, and synchronize tracked command/surface documents from the selected store root.
- Report obsolete documents without deleting them; check freshness without writing documents or indexes.
- Expose public parser help for the supported `init` and `example` commands.
- Split knowledge document definitions into one class per file, keeping public import references and resolving re-exported definitions for template editing.
- Separate follow-up work into self-documentation, store context/federation, and AST ownership/section contracts. No package version bump or publication is included.

## Historical pending changes

- Add reversible `rev,table[...]` template markers for rendering and extracting Markdown tables backed by `list[dict]` fields.
- Add generic cross-store document writes through linked store aliases and federated model namespaces for workflow tools such as `deskops`.

## 0.2.0 - 2026-05-16

- **Store write concurrency**: atomic writes + advisory `fcntl` locks on all index write paths; `--wait` flag for `stores update`
- **Rebuild auditability**: `RebuildReport` dataclass tracks missing docs, empty sections, and unparseable headings in both semantic and section rebuilds; `--verbose` flag for details
- **CLI deprecation surface**: old singular commands (`store`, `model`, `doc`, `ls`, `get`, etc.) emit deprecation warnings; v0.6 was the historical removal target (see freeze note above).
- **Read-side hot path**: `sections show` and `sections fields` prefer persisted index over full IR rebuild; `--rebuild` flag available on `find`/`sections find`
- **Marker ownership robustness**: field name from the canonical `parse_marker()` is validated against known payload paths; unknown markers log a warning

## 0.1.2 - 2026-04-24

- Reorganize the package into `core`, `models`, `runtime`, `cli`, `assets`, and `examples` subpackages while keeping compatibility re-exports
- Add explicit link recovery and transclusion composition with `recover` and `compose`
- Add structural store queries under `st` with `ls`, `get`, `glob`, and `find --where`
- Add store-local semantic indexing under `se` and explicit federated semantic navigation under `gse`
- Add model semantic metadata, canonical model registration, semantic equivalence mapping, and bundled tests for the new workflows

## 0.1.1 - 2026-04-24

- Add current-system architecture docs and diagrams under `docs/architecture/`
- Add feature proposal docs under `desk/` for future SLDB features: link/recover/compose, store tree indexing, semantic DAG indexing, canonical/global-local semantics
- Add desk workspace with task board, self-docs, and operating procedures

## 0.1.0 - 2026-04-21

- Rename the package and CLI from `nldb` to `sldb`
- Add safe-by-default Python marker execution with configurable unsafe mode
- Ship the SLDB example bundle and CLI workflows for extract, render, validate, init, and example
- Add release basics: MIT license, package metadata, and CI
