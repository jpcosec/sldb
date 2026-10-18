---
id: python-sldb-sldb-sldb-api-stores-index_refresh-_trusted
system: sldb
module: sldb.sldb.api.stores.index_refresh
qualname: _trusted
kind: FunctionDef
source_path: sldb/api/stores/index_refresh.py
source_span: 89:99
source_sha256: 52ff82f50024af90f44606255ea3e419ec7c3bf6b714754debcb1a825838e1fc
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.index_refresh:_trusted; contract-sha256:457e3b56d254e0860c777572894c61ce7ff4a3d668968c685606db308acd3349
---

# _trusted

## Signature

_trusted(doc: Any, fresh: str, force: bool)

## Docstring

Whether the stored hashes are enough to skip re-extraction for unchanged text.

A matching source_hash is not enough on its own: a shard written before per-field hashes
existed carries a content_hash nothing verified, and `migrate_hash_names` renames that key
without recomputing it, so trusting it kept a stale content_hash (and a permanent
`data_mutation` in `stores check`) forever, with the Markdown intact. A present field_hashes
map is the evidence that a content_hash came out of the current pipeline; its absence sends
the document through extraction once, which both validates the hash and backfills the map.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.document_field_hashes", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
