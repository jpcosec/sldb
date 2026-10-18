---
id: python-sldb-sldb-store-ops-cascade_store_hash
system: sldb
module: sldb.store.ops
qualname: cascade_store_hash
kind: FunctionDef
source_path: sldb/store/ops.py
source_span: 64:68
source_sha256: 15a1ed96fccad244114a03a10e83846e3c5596b9f5fb9a59a08be3e7211c7e26
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.ops:cascade_store_hash; contract-sha256:841cf43558d4b249d3942a2902a9bc595859395fde41cff6be137c9d743a1949
---

# cascade_store_hash

## Signature

cascade_store_hash(store_path: Path, project_root: Path, store_index: StoreIndex)

## Docstring

Recompute the Merkle root from every model node and persist it.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Recompute the Merkle root from every model node and persist it.

## Architecture

Not documented.
