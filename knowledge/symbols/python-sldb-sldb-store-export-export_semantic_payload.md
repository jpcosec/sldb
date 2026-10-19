---
id: python-sldb-sldb-store-export-export_semantic_payload
system: sldb
module: sldb.store.export
qualname: export_semantic_payload
kind: FunctionDef
source_path: sldb/store/export.py
source_span: 91:93
source_sha256: 1619390e4822af9e09209bb4452ba154c9c3d35735540ec480c0a34555cf7f26
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.export:export_semantic_payload; contract-sha256:724c63d2cf144d78a49d6961c5b9494063eb1940f42e1e5a21b501b151c7a848
---

# export_semantic_payload

## Signature

export_semantic_payload(store_path: Path, project_root: Path, resolve_model_ref: Callable[..., Any] | None=None, pythonpath: str | None=None, *, rebuild: bool=False, command: list[str] | None=None)

## Docstring

Build the `sldb_kgdb_semantic_export` payload from persisted SLDB indexes.

## Imports

["__future__", "datetime", "pathlib", "sldb.store.edge_rebuild", "sldb.store.io", "sldb.store.layout", "sldb.store.package_version", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Build the `sldb_kgdb_semantic_export` payload from persisted SLDB indexes.

## Architecture

Not documented.
