---
id: python-sldb-sldb-sldb-api-model_registry-model_index_writes-rehash_documents
system: sldb
module: sldb.sldb.api.model_registry.model_index_writes
qualname: rehash_documents
kind: FunctionDef
source_path: sldb/api/model_registry/model_index_writes.py
source_span: 52:64
source_sha256: e2e60b0a1efaa0bbb2722d8038f635820fba39a6f9ae7025a1dad875a353f12e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.model_index_writes:rehash_documents;
  contract-sha256:e31657ae58b309ba9dd33dad24cf104a112442d65978f6852b7f6b9827ac0261
---

# rehash_documents

## Signature

rehash_documents(root: Path, d_idx: DocumentsIndex, model_type: type)

## Docstring

Recompute every document's content and field hashes from its Markdown file.

A document that no longer extracts gets an empty field hash, which `stores check`
reports; the broad catch keeps one bad document from aborting the whole reindex.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_lineage", "sldb.api.model_registry.model_reference", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.documents_index", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.semantic_tags"]

## Purpose

Not documented.

## Architecture

Not documented.
