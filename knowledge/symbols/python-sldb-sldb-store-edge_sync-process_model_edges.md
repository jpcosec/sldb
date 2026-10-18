---
id: python-sldb-sldb-store-edge_sync-process_model_edges
system: sldb
module: sldb.store.edge_sync
qualname: process_model_edges
kind: FunctionDef
source_path: sldb/store/edge_sync.py
source_span: '23:36'
source_sha256: 5fd6f57efb17f19c2862f456d18cc176660084d1711fc47c9007c6576b43752b
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_sync:process_model_edges; contract-sha256:3552957fc70696ab8faef63919fa9cad4afe3954800d15e0998ad36dc5c87731
---

# process_model_edges

## Signature

process_model_edges(m_entry, root: Path, report: EdgeRebuildReport, store_path: Path, model_type: Callable[[], Any], build_doc_edges: DocBuilder, full: bool=False)

## Docstring

One model's shards, current. `model_type` imports the class only if the model is walked;
`build_doc_edges(m_entry, model_type, doc)` is edge_rebuild's own document builder; `full`
compares every document's shard whatever the caches say.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.edge_doc_contribution", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.model_contribution", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

One model's shards, current. `model_type` imports the class only if the model is walked; `build_doc_edges(m_entry, model_type, doc)` is edge_rebuild's own document builder; `full` compares every document's shard whatever the caches say.

## Architecture

Not documented.
