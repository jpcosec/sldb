---
id: python-sldb-sldb-sldb-api-documents-payload_save_steps-render_checked
system: sldb
module: sldb.sldb.api.documents.payload_save_steps
qualname: render_checked
kind: FunctionDef
source_path: sldb/api/documents/payload_save_steps.py
source_span: 55:65
source_sha256: f19e94d0ff0a80267b8c651b79582ccc2b22490eebab8773fb35e49fd05d95eb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.payload_save_steps:render_checked;
  contract-sha256:e74bb878c792967a9a268fbb4d2ef2893c3a8c67d4fb584e4ae6a985d40b990d
---

# render_checked

## Signature

render_checked(model_type: type, payload: dict[str, Any], ref_root: Path)

## Docstring

The payload rendered to Markdown, refused unless it round-trips.

`ref_root` is the project root, so a composed field resolves its refs against the project
rather than against whatever directory the caller happens to run in.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
