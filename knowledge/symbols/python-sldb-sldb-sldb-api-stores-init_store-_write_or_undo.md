---
id: python-sldb-sldb-sldb-api-stores-init_store-_write_or_undo
system: sldb
module: sldb.sldb.api.stores.init_store
qualname: _write_or_undo
kind: FunctionDef
source_path: sldb/api/stores/init_store.py
source_span: 53:63
source_sha256: 093bd3453d72151b1d8fb6afa508d3b6d7ec7c929e92ef28238a78eb783e6671
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.init_store:_write_or_undo; contract-sha256:b4bb43c9c605cab81766a19a966f4793ec82b3583aaba5cfbf3beeb3f5f65d30
---

# _write_or_undo

## Signature

_write_or_undo(store_path: Path)

## Docstring

Write the empty store, or remove what was written and say why: a failed init used to
leave a partial `.sldb/` and a bare `Unexpected: [Errno 13]` (deskops, inbox 20260614-000000).

## Imports

["__future__", "pathlib", "shutil", "sldb.api.stores.store_location", "sldb.api.stores.store_skeleton", "sldb.core.exceptions", "sldb.store.layout"]

## Purpose

Not documented.

## Architecture

Not documented.
