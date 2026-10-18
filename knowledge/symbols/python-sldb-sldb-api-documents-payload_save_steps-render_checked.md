---
id: python-sldb-sldb-api-documents-payload_save_steps-render_checked
system: sldb
module: sldb.api.documents.payload_save_steps
qualname: render_checked
kind: FunctionDef
source_path: sldb/api/documents/payload_save_steps.py
source_span: 55:65
source_sha256: f19e94d0ff0a80267b8c651b79582ccc2b22490eebab8773fb35e49fd05d95eb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.payload_save_steps:render_checked;
  contract-sha256:188d06683c8fe5b686cc8d1d1e891eff21e158d800eef03084f4e38552b272b0
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
