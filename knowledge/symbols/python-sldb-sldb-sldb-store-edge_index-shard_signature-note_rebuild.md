---
id: python-sldb-sldb-sldb-store-edge_index-shard_signature-note_rebuild
system: sldb
module: sldb.sldb.store.edge_index.shard_signature
qualname: note_rebuild
kind: FunctionDef
source_path: sldb/store/edge_index/shard_signature.py
source_span: '16:19'
source_sha256: 19a4672a665f01101b61e92098c68565b8eca1103ad9071bfa0192d71373525c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_index.shard_signature:note_rebuild;
  contract-sha256:4aa51c1e559c2cfdf3eb1d727c5ccb5edc013e24ce6d3876b5bd8a70766eb9d9
---

# note_rebuild

## Signature

note_rebuild(store_path: Path)

## Docstring

This process just rewrote shards of that store: two writes inside one mtime tick must
still read as two states.

## Imports

["__future__", "os", "pathlib", "sldb.store.layout"]

## Purpose

Not documented.

## Architecture

Not documented.
