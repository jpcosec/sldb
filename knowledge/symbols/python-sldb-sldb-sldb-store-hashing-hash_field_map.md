---
id: python-sldb-sldb-sldb-store-hashing-hash_field_map
system: sldb
module: sldb.sldb.store.hashing
qualname: hash_field_map
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: '41:47'
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.hashing:hash_field_map; contract-sha256:5a00453b19682d6a39a549ed06d783a517a99e1c73396d7af32d504291877917
---

# hash_field_map

## Signature

hash_field_map(model_type: Any, markdown_text: str, codec: StoreCodec=default_codec)

## Docstring

`hash_field_map_of` for text that has not been extracted yet.

Prefer `hash_field_map_of` where the payload is already in hand (`index_refresh` caches
it): extraction is the expensive half, and this would pay it twice.

## Imports

["hashlib", "json", "sldb.store.codec", "sldb.store.models", "sldb.store.semantic_tags", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
