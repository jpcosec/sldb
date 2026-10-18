---
id: python-sldb-sldb-sldb-store-runtime_cache-payload_of
system: sldb
module: sldb.sldb.store.runtime_cache
qualname: payload_of
kind: FunctionDef
source_path: sldb/store/runtime_cache.py
source_span: 92:102
source_sha256: 870a33b2e031d380c875372e22bbf508b533af2cbd6dae4f59d6ddb6e563db78
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.runtime_cache:payload_of; contract-sha256:94899357ebcc56f350de65e22a5bf292b3dda69de948f60aa1f87f3df335fb1b
---

# payload_of

## Signature

payload_of(rel_path: str, hash_c: str, model_type: type)

## Docstring

The extracted payload of this text under this model class, as the cache knows it now.

Matched on the class itself, not on its name: a payload is what a class extracts from a
text, and two classes called `Spec` in two modules extract different things. Matching the
name let `content_hash` — which is persisted — be computed from another class's payload.

## Imports

["__future__", "dataclasses", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.runtime_cache_signature", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
