---
id: python-sldb-sldb-store-hashing-hash_fields_with_map
system: sldb
module: sldb.store.hashing
qualname: hash_fields_with_map
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: '50:59'
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.hashing:hash_fields_with_map; contract-sha256:3d5b0c5c367a9ea41afc6567f1766b9a25718bafc0bf3b0a40e82dd08909ddc8
---

# hash_fields_with_map

## Signature

hash_fields_with_map(model_type: Any, markdown_text: str, codec: StoreCodec=default_codec)

## Docstring

A document's `content_hash` and its per-field map, from a single extraction.

What a write site wants: calling `hash_fields` and `hash_field_map` separately would
extract the same text twice.

## Imports

["hashlib", "json", "sldb.store.codec", "sldb.store.models", "sldb.store.semantic_tags", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
