---
id: python-sldb-sldb-sldb-store-io-rollback-rollback_on_error
system: sldb
module: sldb.sldb.store.io.rollback
qualname: rollback_on_error
kind: FunctionDef
source_path: sldb/store/io/rollback.py
source_span: '11:21'
source_sha256: c63bc2f2ea04b8d5ce459cddbe24366bfc223d01277bd20c5c221c851fd37806
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io.rollback:rollback_on_error; contract-sha256:8ac0fe10f8eb5809f32f30b31d6cb1635d5d6a1db777cfdfece26d7b3a56861e
---

# rollback_on_error

## Signature

rollback_on_error(paths: list[Path], forget_caches: Callable[[], None])

## Docstring

Snapshot `paths`; if the block raises, restore their bytes (or absence), call
`forget_caches` so no in-memory copy outlives the restore, and re-raise.

## Imports

["__future__", "contextlib", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
