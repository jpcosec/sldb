# Changelog

Version note (2026-09-13): this working tree declares package version `0.1.0` in `pyproject.toml`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

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
