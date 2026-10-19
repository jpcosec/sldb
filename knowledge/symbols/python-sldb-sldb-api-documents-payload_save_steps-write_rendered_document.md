---
id: python-sldb-sldb-api-documents-payload_save_steps-write_rendered_document
system: sldb
module: sldb.api.documents.payload_save_steps
qualname: write_rendered_document
kind: FunctionDef
source_path: sldb/api/documents/payload_save_steps.py
source_span: 68:72
source_sha256: f19e94d0ff0a80267b8c651b79582ccc2b22490eebab8773fb35e49fd05d95eb
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.payload_save_steps:write_rendered_document;
  contract-sha256:a2bae32a3300e937ffbcf256114138d78c389611d567f3fedef0c514c1e9cea2
---

# write_rendered_document

## Signature

write_rendered_document(root: Path, doc_entry: DocumentEntry, model_type: type, rendered: str)

## Docstring

Write the rendered Markdown (plus final newline) and record its source and content hashes.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Write the rendered Markdown (plus final newline) and record its source and content hashes.

## Architecture

Not documented.
