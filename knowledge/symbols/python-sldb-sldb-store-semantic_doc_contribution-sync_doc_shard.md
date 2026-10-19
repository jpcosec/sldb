---
id: python-sldb-sldb-store-semantic_doc_contribution-sync_doc_shard
system: sldb
module: sldb.store.semantic_doc_contribution
qualname: sync_doc_shard
kind: FunctionDef
source_path: sldb/store/semantic_doc_contribution.py
source_span: '26:38'
source_sha256: 3c7c97055e1e1c32638f99f7b51a7d3aeb2dde51dc5986ebba056a93fa4b14c7
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.semantic_doc_contribution:sync_doc_shard;
  contract-sha256:fa7594d9864ae552a4ee3fd3720e5ed61dcb87e52b6ea572ddd4aba94d162941
---

# sync_doc_shard

## Signature

sync_doc_shard(store_path, doc, d_path, m_entry, resolver, py_path, report)

## Docstring

This document's semantic shard, current: reused untouched when its `source_hash` already
matches what the shard on disk carries, (re)extracted and (re)written otherwise.

## Imports

["__future__", "sldb.store.codec", "sldb.store.exceptions", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.models", "sldb.store.semantic_doc_tags"]

## Purpose

This document's semantic shard, current: reused untouched when its `source_hash` already matches what the shard on disk carries, (re)extracted and (re)written otherwise.

## Architecture

Not documented.
