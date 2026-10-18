---
id: python-sldb-sldb-sldb-store-edge_index-store_contribution-build_store_edges
system: sldb
module: sldb.sldb.store.edge_index.store_contribution
qualname: build_store_edges
kind: FunctionDef
source_path: sldb/store/edge_index/store_contribution.py
source_span: '11:30'
source_sha256: 43b1375b11fe8016e7f60ca2130355ab2900ab869315fbc3bf6fba3f6819260b
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_index.store_contribution:build_store_edges;
  contract-sha256:ebe42a1fbbb1853e9aa429603dd3e3876a28dddf292853a587a73e97ee9ad0bd
---

# build_store_edges

## Signature

build_store_edges(st_idx: StoreIndex, dag: SemanticDAG)

## Docstring

The store's shard. The store node carries no path and no `store_hash`: a shard must read the
same wherever the project is checked out, and `store_hash` is already the store index's.

Args:
    st_idx: The store index (its registered models).
    dag: The semantic DAG (tag parents and cross-store equivalences).

Returns:
    The shard, not yet stamped with `edges_version`.

## Imports

["__future__", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.records", "sldb.store.models"]

## Purpose

Not documented.

## Architecture

Not documented.
