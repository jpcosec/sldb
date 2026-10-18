---
id: python-sldb-sldb-store-edge_index-validation-validate_edge_index_by_store
system: sldb
module: sldb.store.edge_index.validation
qualname: validate_edge_index_by_store
kind: FunctionDef
source_path: sldb/store/edge_index/validation.py
source_span: '32:45'
source_sha256: 03c609667a78e9116e3dc13b69649e8b0aa72d0690774488e6c79d05d6c9d81e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.validation:validate_edge_index_by_store;
  contract-sha256:8dd703434138e7f4101fce0ec1d0e006a98e51d7b22e6ad3cdfc5d80b7f8c71d
---

# validate_edge_index_by_store

## Signature

validate_edge_index_by_store(index: EdgeIndex)

## Docstring

(violations of this store's own edges, those only a linked store's edges commit).

A cardinality violation is this store's when any edge behind it is; an edge a linked store
contributes that this store also contributes (a shared model's fields) is this store's.

## Imports

["__future__", "collections", "sldb.store.edge_index.edge_index", "sldb.store.edge_index.resolve", "sldb.store.model_contract", "sldb.store.models", "typing"]

## Purpose

(violations of this store's own edges, those only a linked store's edges commit).

## Architecture

Not documented.
