---
id: python-sldb-sldb-store-io-rollback-rollback_on_error
system: sldb
module: sldb.store.io.rollback
qualname: rollback_on_error
kind: FunctionDef
source_path: sldb/store/io/rollback.py
source_span: '11:21'
source_sha256: c63bc2f2ea04b8d5ce459cddbe24366bfc223d01277bd20c5c221c851fd37806
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.io.rollback:rollback_on_error; contract-sha256:35df7c086dac3ef7a70cad6c598d58deb9e9de77598c2f1099438162ca347ca1
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

Snapshot `paths`; if the block raises, restore their bytes (or absence), call `forget_caches` so no in-memory copy outlives the restore, and re-raise.

## Architecture

Not documented.
