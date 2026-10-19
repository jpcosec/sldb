---
id: python-sldb-sldb-store-edge_rebuild-_prune_models
system: sldb
module: sldb.store.edge_rebuild
qualname: _prune_models
kind: FunctionDef
source_path: sldb/store/edge_rebuild.py
source_span: 71:80
source_sha256: 7f2cc97ef06264e2fd1d5e896d4869aa7123ad7334505b0744f0e3fa53108880
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_rebuild:_prune_models; contract-sha256:57238796c67ff21751f9c637322c2d6090bedba160739be12192cac9830f8cc0
---

# _prune_models

## Signature

_prune_models(store_path: Path, registered: set[str])

## Docstring

Shards of a model that is no longer registered go with it: its file and its directory.

## Imports

["__future__", "logging", "pathlib", "sldb.store.codec", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.doc_contribution", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.shard_signature", "sldb.store.edge_index.store_contribution", "sldb.store.edge_sync", "sldb.store.exceptions", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

Shards of a model that is no longer registered go with it: its file and its directory.

## Architecture

Not documented.
