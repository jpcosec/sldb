---
id: python-sldb-sldb-api-edges-unresolved_references-unresolved_references
system: sldb
module: sldb.api.edges.unresolved_references
qualname: unresolved_references
kind: FunctionDef
source_path: sldb/api/edges/unresolved_references.py
source_span: '12:28'
source_sha256: fe28d882f7f6d1e12443b6682b8e5f82ce21698305fe866723ee79a38ff2c746
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.edges.unresolved_references:unresolved_references;
  contract-sha256:d12f0696738e94fb05dd3e82b8038c8a204b23f512ebebe42b494ee8c797cc72
---

# unresolved_references

## Signature

unresolved_references(store: str | Path | None, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

Every value of a declared reference or containment field that names no document.

A value resolves as an export id (`Model:name`), as the path of a tracked document, or as
`Model:value` for the one model the field allows that has it (`__reference_models__`,
`__containment__`). What is left is reported here and never stored as an edge; a free
reference field only reports export ids.

Args:
    store: The store (path, alias, or None to discover it).
    include_linked: Also read the linked stores' documents, their ids qualified by name.
    exclude_tags: Leave out the documents carrying one of these tags.

Returns:
    One record per unresolved value, in index order.

## Imports

["__future__", "pathlib", "sldb.api.edges.edge_reading", "sldb.store.edge_index.unresolved_reference", "typing"]

## Purpose

Every value of a declared reference or containment field that names no document.

## Architecture

Not documented.
