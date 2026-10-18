---
id: python-sldb-sldb-sldb-store-hashing-hash_fields_with_map
system: sldb
module: sldb.sldb.store.hashing
qualname: hash_fields_with_map
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: '50:59'
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.hashing:hash_fields_with_map; contract-sha256:5e9a6ca03ce10dcf8e7574118a462dae8a10e9ee2a7d785f3eddf8cba2476385
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
