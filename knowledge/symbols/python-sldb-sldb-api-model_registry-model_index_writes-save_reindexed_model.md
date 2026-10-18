---
id: python-sldb-sldb-api-model_registry-model_index_writes-save_reindexed_model
system: sldb
module: sldb.api.model_registry.model_index_writes
qualname: save_reindexed_model
kind: FunctionDef
source_path: sldb/api/model_registry/model_index_writes.py
source_span: 67:78
source_sha256: e2e60b0a1efaa0bbb2722d8038f635820fba39a6f9ae7025a1dad875a353f12e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_index_writes:save_reindexed_model;
  contract-sha256:2e873cc63324c8c8df9875a7d4ca7ac2cce583eb0a6d5dfc438780d00ffe0c74
---

# save_reindexed_model

## Signature

save_reindexed_model(sp: Path, root: Path, idx: StoreIndex, m_entry: ModelEntry, m_idx: ModelsIndex, d_idx: DocumentsIndex, bump_version: bool, pythonpath: str | None, model_type: type | None=None)

## Docstring

Persist a reindexed model's indexes (bumping its version if asked) and rebuild derived indexes.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_lineage", "sldb.api.model_registry.model_reference", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.documents_index", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.semantic_tags"]

## Purpose

Persist a reindexed model's indexes (bumping its version if asked) and rebuild derived indexes.

## Architecture

Not documented.
