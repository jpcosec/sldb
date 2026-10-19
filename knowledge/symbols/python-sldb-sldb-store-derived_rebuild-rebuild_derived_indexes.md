---
id: python-sldb-sldb-store-derived_rebuild-rebuild_derived_indexes
system: sldb
module: sldb.store.derived_rebuild
qualname: rebuild_derived_indexes
kind: FunctionDef
source_path: sldb/store/derived_rebuild.py
source_span: '13:24'
source_sha256: 4892743c7d55e1fa24b816cfbc950ca001a66b4bedbdbae77f6a688e15393ba7
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.derived_rebuild:rebuild_derived_indexes;
  contract-sha256:b8dc17bb53ff872c10fa8ef680caabf08989ae2037d8eb96248118c6dd435c5a
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

Semantic, sections and edges indexes brought current; used where a model (not one document) changed — registered, reindexed, promoted — so its node, fields and every document hash that moved reach the edge index in the same operation.

## Architecture

Not documented.
