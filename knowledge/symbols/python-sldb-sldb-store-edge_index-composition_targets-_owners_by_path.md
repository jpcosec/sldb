---
id: python-sldb-sldb-store-edge_index-composition_targets-_owners_by_path
system: sldb
module: sldb.store.edge_index.composition_targets
qualname: _owners_by_path
kind: FunctionDef
source_path: sldb/store/edge_index/composition_targets.py
source_span: '37:49'
source_sha256: 118734ea5c34dedef233d1956c6a6e4008fe682a9b14383086f4122171be1d54
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.composition_targets:_owners_by_path;
  contract-sha256:0b29674f5780abc4ca99bea35f50d04052937b4648b58f4d416eaed0518f2ca0
---

# _owners_by_path

## Signature

_owners_by_path(nodes: dict[str, EdgeNodeRecord])

## Docstring

Project-relative path -> node id of the document tracked at it.

A linked store's documents are left out: its paths are relative to its own root, so the
same path can name a document in each store and a ref means the composing store's one.

## Imports

["__future__", "posixpath", "sldb.store.edge_index.composition_edges", "sldb.store.models"]

## Purpose

Project-relative path -> node id of the document tracked at it.

## Architecture

Not documented.
