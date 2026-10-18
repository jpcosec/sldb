---
id: python-sldb-sldb-sldb-store-edge_doc_contribution-sync_doc_shard
system: sldb
module: sldb.sldb.store.edge_doc_contribution
qualname: sync_doc_shard
kind: FunctionDef
source_path: sldb/store/edge_doc_contribution.py
source_span: '17:29'
source_sha256: d96d9dd3ee901bf13270c475186e4c27f4729c50a55ea60f753ef698c77ab28b
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_doc_contribution:sync_doc_shard;
  contract-sha256:82bd6a51928163b715bb049c459f06dbe0c89ce91d172b94c398c6da935d799c
---

# sync_doc_shard

## Signature

sync_doc_shard(store_path, doc: DocumentEntry, m_entry, report: EdgeRebuildReport, build_doc_edges: Callable[[DocumentEntry], DocEdges], contract: str='')

## Docstring

This document's edges shard, current: reused untouched when it was built from this
`source_hash` (and these tags, under these rules), rebuilt and rewritten otherwise.
`build_doc_edges` is edge_rebuild's own builder, passed in rather than imported back.

## Imports

["__future__", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
