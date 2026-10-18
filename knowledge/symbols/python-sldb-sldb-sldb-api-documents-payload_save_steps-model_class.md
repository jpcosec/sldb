---
id: python-sldb-sldb-sldb-api-documents-payload_save_steps-model_class
system: sldb
module: sldb.sldb.api.documents.payload_save_steps
qualname: model_class
kind: FunctionDef
source_path: sldb/api/documents/payload_save_steps.py
source_span: '27:35'
source_sha256: f19e94d0ff0a80267b8c651b79582ccc2b22490eebab8773fb35e49fd05d95eb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.payload_save_steps:model_class;
  contract-sha256:5c70209c1e5f6e99128d33ff4e073c536a365e3afdbd6a49a4836655c284b70c
---

# model_class

## Signature

model_class(model_ref: str, pythonpath: str | None, root: Path)

## Docstring

The model class, imported with the caller's pythonpath first, then the store's own root.

A linked store's models import from where that store lives.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
