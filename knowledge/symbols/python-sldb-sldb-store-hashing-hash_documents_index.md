---
id: python-sldb-sldb-store-hashing-hash_documents_index
system: sldb
module: sldb.store.hashing
qualname: hash_documents_index
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: 62:68
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.hashing:hash_documents_index; contract-sha256:84ac4cfb7386863d233d4a93bd36c981e680cbdfd3b2e04bca66ad88621a1ded
---

# hash_documents_index

## Signature

hash_documents_index(documents_index: DocumentsIndex)

## Docstring

PLAN 15 capa 7: keyed by `name` and sorted — order-independent (documents_index.
documents used to be insertion-ordered, so roster_hash used to depend on write order too; a
store's Merkle root should depend only on content). The same value however documents
were gathered: a full scan (stores update) or the incremental per-document child-hash
map (sldb.store.documents_hash — a write's own hot path).

## Imports

["hashlib", "json", "sldb.store.codec", "sldb.store.models", "sldb.store.semantic_tags", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
