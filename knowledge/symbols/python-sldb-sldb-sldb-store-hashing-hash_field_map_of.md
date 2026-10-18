---
id: python-sldb-sldb-sldb-store-hashing-hash_field_map_of
system: sldb
module: sldb.sldb.store.hashing
qualname: hash_field_map_of
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: '24:38'
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.hashing:hash_field_map_of; contract-sha256:63e08b454d84d0c2fcd3982a6063508b39cff59b192a8006d9afc254b9461026
---

# hash_field_map_of

## Signature

hash_field_map_of(payload: dict[str, Any])

## Docstring

One hash per field of an already extracted payload.

`content_hash` signs the payload as a whole, so a single changed field moves it and
nothing says which one. This signs each field on its own: a diff against the map an index
holds names the fields that actually moved, which is what `stores check` reports and what
a per-field consumer (an embedding index keyed `Model/doc#field`) needs to re-embed one
field instead of all of them.

Each value goes through `hash_payload`, so a field's hash is the same function of its value
that `content_hash` is of the whole payload: order-independent for dicts, exact for scalars.
This is a sibling of `content_hash`, never a replacement — `content_hash` stays the
optimistic-concurrency token `/save` compares against `expected`.

## Imports

["hashlib", "json", "sldb.store.codec", "sldb.store.models", "sldb.store.semantic_tags", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
