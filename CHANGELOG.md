# Changelog

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
