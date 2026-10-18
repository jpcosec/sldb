---
id: python-sldb-sldb-sldb-store-derived_rebuild-rebuild_derived_indexes
system: sldb
module: sldb.sldb.store.derived_rebuild
qualname: rebuild_derived_indexes
kind: FunctionDef
source_path: sldb/store/derived_rebuild.py
source_span: '13:24'
source_sha256: 4892743c7d55e1fa24b816cfbc950ca001a66b4bedbdbae77f6a688e15393ba7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.derived_rebuild:rebuild_derived_indexes;
  contract-sha256:aa3e197998cc8b25795e8fccb46ae80088f829369e8834a6b560db5f5f5d482b
---

# rebuild_derived_indexes

## Signature

rebuild_derived_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None=None)

## Docstring

Semantic, sections and edges indexes brought current; used where a model (not one
document) changed — registered, reindexed, promoted — so its node, fields and every
document hash that moved reach the edge index in the same operation.

Returns:
    The semantic rebuild's report (what those callers already reported).

## Imports

["__future__", "pathlib", "sldb.store.edge_rebuild", "sldb.store.section_rebuild", "sldb.store.semantic"]

## Purpose

Not documented.

## Architecture

Not documented.
