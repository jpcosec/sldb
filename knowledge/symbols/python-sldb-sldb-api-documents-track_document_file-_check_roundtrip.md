---
id: python-sldb-sldb-api-documents-track_document_file-_check_roundtrip
system: sldb
module: sldb.api.documents.track_document_file
qualname: _check_roundtrip
kind: FunctionDef
source_path: sldb/api/documents/track_document_file.py
source_span: 63:67
source_sha256: 3a634c8ce898154af6bda2f7a29dd8bdbbc892e92d6988ff05052d6c3d2856c8
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.track_document_file:_check_roundtrip;
  contract-sha256:7ce1647b3cb9cefd907bb66f1c9e97c2ac5b6d94f533037c1a96b4747681de9b
---

# _check_roundtrip

## Signature

_check_roundtrip(model_type: type, doc_path: Path)

## Docstring

Refuse a file that does not extract and re-render identically under the model.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.frontmatter_keys", "sldb.api.documents.refuse_structural_noise", "sldb.api.journal", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.ops"]

## Purpose

Refuse a file that does not extract and re-render identically under the model.

## Architecture

Not documented.
