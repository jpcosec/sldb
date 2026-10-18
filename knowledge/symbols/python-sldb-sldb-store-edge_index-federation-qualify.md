---
id: python-sldb-sldb-store-edge_index-federation-qualify
system: sldb
module: sldb.store.edge_index.federation
qualname: qualify
kind: FunctionDef
source_path: sldb/store/edge_index/federation.py
source_span: '41:48'
source_sha256: 8035b477af7ddc4e0a2a164daecf0883269b3012570643e3bb3e6591795e78c9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.federation:qualify; contract-sha256:dd7cc209c67840badc1df73238a51988bf4876b9f02ee0499bc8a00471471ac8
---

# qualify

## Signature

qualify(part: EdgeContribution, store_name: str | None)

## Docstring

A linked store's contribution with every id qualified and every edge marked `from_store`
(so a check of this store tells its own edges from its links'); the local store's, untouched.

## Imports

["__future__", "pathlib", "sldb.store.edge_index.node_ids", "sldb.store.models"]

## Purpose

A linked store's contribution with every id qualified and every edge marked `from_store` (so a check of this store tells its own edges from its links'); the local store's, untouched.

## Architecture

Not documented.
