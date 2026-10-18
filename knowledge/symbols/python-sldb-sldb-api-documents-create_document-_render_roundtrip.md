---
id: python-sldb-sldb-api-documents-create_document-_render_roundtrip
system: sldb
module: sldb.api.documents.create_document
qualname: _render_roundtrip
kind: FunctionDef
source_path: sldb/api/documents/create_document.py
source_span: 71:81
source_sha256: 07562f9e0386f4073f011adfb675433b0c0c84363b1b2c1540ef7b2f0127d465
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.create_document:_render_roundtrip;
  contract-sha256:40718849f9c4c1d01b4fb6e54cc86b75f94fc8bd4823e54e8221933547b0170d
---

# _render_roundtrip

## Signature

_render_roundtrip(model_type: type, payload: dict[str, Any], ref_root: Path)

## Docstring

The payload rendered to Markdown, refused unless it extracts back identically.

`ref_root` is the project root, so a composed field resolves its refs the way the project
names them; without it they would resolve against whatever directory the caller runs in.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.frontmatter_keys", "sldb.api.documents.refuse_structural_noise", "sldb.api.journal", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.ops", "typing"]

## Purpose

The payload rendered to Markdown, refused unless it extracts back identically.

## Architecture

Not documented.
