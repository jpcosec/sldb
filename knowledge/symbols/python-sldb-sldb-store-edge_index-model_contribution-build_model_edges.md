---
id: python-sldb-sldb-store-edge_index-model_contribution-build_model_edges
system: sldb
module: sldb.store.edge_index.model_contribution
qualname: build_model_edges
kind: FunctionDef
source_path: sldb/store/edge_index/model_contribution.py
source_span: '12:32'
source_sha256: b71f267e519ad234243de3c4d190684002d685a5da93619c0c97f83d6cdd6fa5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.model_contribution:build_model_edges;
  contract-sha256:9b41be67c59f845051f4d89c9c0c1274016b3f65e0edf35c872ea8c6a00c072d
---

# build_model_edges

## Signature

build_model_edges(m_idx: ModelsIndex, model_type: Any | None)

## Docstring

The model's shard. `roster_hash` is left out of the node on purpose: it moves with every
document write, and the documents' own shards already carry their hashes.

Args:
    m_idx: The model's index record (ref, path, version, semantics, base models).
    model_type: The imported model class, or None when it cannot be imported here (a
        linked store's model): the node is still contributed, its fields are not.

Returns:
    The shard, not yet stamped with `edges_version`.

## Imports

["__future__", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.records", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
