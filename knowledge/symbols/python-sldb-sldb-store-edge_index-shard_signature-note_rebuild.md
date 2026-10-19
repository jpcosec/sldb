---
id: python-sldb-sldb-store-edge_index-shard_signature-note_rebuild
system: sldb
module: sldb.store.edge_index.shard_signature
qualname: note_rebuild
kind: FunctionDef
source_path: sldb/store/edge_index/shard_signature.py
source_span: '16:19'
source_sha256: 19a4672a665f01101b61e92098c68565b8eca1103ad9071bfa0192d71373525c
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.shard_signature:note_rebuild;
  contract-sha256:9cdb22781dbb82c4908e2cd57d3f6c9cd37a26d4eb55fadd903382df80ac7b60
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

This process just rewrote shards of that store: two writes inside one mtime tick must still read as two states.

## Architecture

Not documented.
