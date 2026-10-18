---
id: python-sldb-sldb-api-model_registry-model_index_writes-write_new_model_indexes
system: sldb
module: sldb.api.model_registry.model_index_writes
qualname: write_new_model_indexes
kind: FunctionDef
source_path: sldb/api/model_registry/model_index_writes.py
source_span: '29:42'
source_sha256: e2e60b0a1efaa0bbb2722d8038f635820fba39a6f9ae7025a1dad875a353f12e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_index_writes:write_new_model_indexes;
  contract-sha256:e8ef6ff347f5c54de0ee3a4ee5fdcf420ff09a0bfe312a33bdd166241e10ddcb
---

# write_new_model_indexes

## Signature

write_new_model_indexes(sp: Path, root: Path, idx: StoreIndex, model_type: type, model_ref: str, m_path: str, mi_rel: str, di_rel: str, canonical: bool, pythonpath: str | None)

## Docstring

Register a model: empty documents index, models index, store entry, semantic rebuild.

The roster hash starts as hash_documents_index of the empty index, not "" -- an unhashed
empty string fails `stores check` until `models update` runs.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_lineage", "sldb.api.model_registry.model_reference", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.documents_index", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.semantic_tags"]

## Purpose

Not documented.

## Architecture

Not documented.
