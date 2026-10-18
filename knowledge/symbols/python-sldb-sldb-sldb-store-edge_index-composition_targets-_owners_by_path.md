---
id: python-sldb-sldb-sldb-store-edge_index-composition_targets-_owners_by_path
system: sldb
module: sldb.sldb.store.edge_index.composition_targets
qualname: _owners_by_path
kind: FunctionDef
source_path: sldb/store/edge_index/composition_targets.py
source_span: '37:49'
source_sha256: 118734ea5c34dedef233d1956c6a6e4008fe682a9b14383086f4122171be1d54
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_index.composition_targets:_owners_by_path;
  contract-sha256:52490fae4cc4cf18c00344fe0d03d4ba44405b4c784ea6774df76acb52cfe4b9
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

Not documented.

## Architecture

Not documented.
