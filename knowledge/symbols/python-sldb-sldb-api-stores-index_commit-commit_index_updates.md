---
id: python-sldb-sldb-api-stores-index_commit-commit_index_updates
system: sldb
module: sldb.api.stores.index_commit
qualname: commit_index_updates
kind: FunctionDef
source_path: sldb/api/stores/index_commit.py
source_span: '22:45'
source_sha256: 0b2f2196939a4d5e718b1616d720f365b2b844242b0e475f17deca3b46ee4cb8
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.index_commit:commit_index_updates; contract-sha256:1088f3f6f506172bcc69f3e64e7a796e854d7bf205a175ffa2159d8139178d78
---

# commit_index_updates

## Signature

commit_index_updates(sp: Path, root: Path, idx: StoreIndex, pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]], pythonpath: str | None, wait: bool)

## Docstring

Persist every queued model's indexes, then rebuild semantic and section indexes.

Args:
    sp: The store's `.sldb` directory.
    root: The store's project root.
    idx: The store index whose store_hash is recomputed at the end.
    pending: (model entry, models index, documents index, model class) tuples to save.
    changed: Documents whose hashes moved, by model name.
    pythonpath: Import root for the store's model modules.
    wait: Wait for the store lock instead of failing when it is held.

Returns:
    The semantic and sections rebuild reports.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Persist every queued model's indexes, then rebuild semantic and section indexes.

## Architecture

Not documented.
