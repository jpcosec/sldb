---
id: python-sldb-sldb-sldb-api-edges-check_edges-check_edges
system: sldb
module: sldb.sldb.api.edges.check_edges
qualname: check_edges
kind: FunctionDef
source_path: sldb/api/edges/check_edges.py
source_span: '14:31'
source_sha256: 4e8e5c477826ac2ffac3a2925b8fd9fd0afe22fa0a37fc1650a9eb0ddf4ddfa3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.edges.check_edges:check_edges; contract-sha256:fbc5f02d55adb17c32fa88fa70d9cfba32ecee0f8332bd9a4ba091de0650800e
---

# check_edges

## Signature

check_edges(store: str | Path | None, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

The cross-document validation of the edge index, as a report.

Args:
    store: The store (path, alias, or None to discover it).
    include_linked: Validate the federated index, not just the local store's.
    exclude_tags: Leave out the documents carrying one of these tags before validating.

Returns:
    The errors found (the same sentences TypedIngestError carried, plus a cycle in a
    relation that must be acyclic) and the stale documents, this store's apart from those
    only its linked stores' edges commit (`linked_errors`, `linked_stale`: not a failure here).

## Imports

["__future__", "pathlib", "sldb.api.edges.edge_check_report", "sldb.api.edges.edge_reading", "sldb.store.edge_index.acyclic", "sldb.store.edge_index.validation", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
