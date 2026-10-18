---
id: python-sldb-sldb-api-documents-document_lookup-find_doc
system: sldb
module: sldb.api.documents.document_lookup
qualname: find_doc
kind: FunctionDef
source_path: sldb/api/documents/document_lookup.py
source_span: '21:39'
source_sha256: 610537428c389e86f08db49ef8aaf0f5feae27b82321f23467ced296a949c499
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.document_lookup:find_doc; contract-sha256:c38a624db94a156a6f6ab0efb3c241fc0647c4a10cdf480cd22611f08ec12cec
---

# find_doc

## Signature

find_doc(sp: Path, root: Path, idx: StoreIndex, doc_ref: str)

## Docstring

The model entry, models index and document entry of a tracked document.

`doc_ref` is usually a name: one cheap shard check per model. A path may be given as the
store recorded it (relative to the project root) or absolute. Falling back to a match
by path uses this operation's own cached entries (PLAN 15 capa 8: a doc found by name
never pays for that; a fallback within an already-composed operation pays nothing new).

Raises:
    SLDBError: When no model tracks a document with that name or path.

## Imports

["__future__", "pathlib", "sldb.core.exceptions", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index"]

## Purpose

Not documented.

## Architecture

Not documented.
