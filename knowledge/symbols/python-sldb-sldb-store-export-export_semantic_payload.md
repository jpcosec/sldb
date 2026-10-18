---
id: python-sldb-sldb-store-export-export_semantic_payload
system: sldb
module: sldb.store.export
qualname: export_semantic_payload
kind: FunctionDef
source_path: sldb/store/export.py
source_span: 87:89
source_sha256: fe78991a46bf0d7d5f5f00cda9a2598fbdc212cf89ef327c727174f30cd8a1e0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.export:export_semantic_payload; contract-sha256:cfa63a50528da132a2afe9ba9870b8b6d3a4c67bbe4567e6a4c44b1a2c28ccfb
---

# export_semantic_payload

## Signature

export_semantic_payload(store_path: Path, project_root: Path, resolve_model_ref: Callable[..., Any] | None=None, pythonpath: str | None=None, *, rebuild: bool=False, command: list[str] | None=None)

## Docstring

Build the `sldb_semantic_export` payload from persisted SLDB indexes.

## Imports

["__future__", "datetime", "pathlib", "sldb.store.edge_rebuild", "sldb.store.io", "sldb.store.layout", "sldb.store.package_version", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Build the `sldb_semantic_export` payload from persisted SLDB indexes.

## Architecture

Not documented.
