---
id: python-sldb-sldb-sldb-api-documents-payload_save_steps-save_document_indexes
system: sldb
module: sldb.sldb.api.documents.payload_save_steps
qualname: save_document_indexes
kind: FunctionDef
source_path: sldb/api/documents/payload_save_steps.py
source_span: 75:90
source_sha256: f19e94d0ff0a80267b8c651b79582ccc2b22490eebab8773fb35e49fd05d95eb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.payload_save_steps:save_document_indexes;
  contract-sha256:5bdbe1fedb35092b2e9c63d3b15465284adb0572060d964952cfb68105304c37
---

# save_document_indexes

## Signature

save_document_indexes(sp: Path, root: Path, idx: StoreIndex, m_idx: ModelsIndex, m_entry: ModelEntry, doc_entry: DocumentEntry, pythonpath: str | None, model_type: type | None=None)

## Docstring

Save the document shard and model hashes, then rebuild derived indexes, under the store lock.

The model's roster hash covers its documents' hashes: a field write must move it, or
`stores check` fails and consumers keyed on the model node never see the change.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
