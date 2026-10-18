---
id: python-sldb-sldb-store-section_doc_contribution-sync_doc_shard
system: sldb
module: sldb.store.section_doc_contribution
qualname: sync_doc_shard
kind: FunctionDef
source_path: sldb/store/section_doc_contribution.py
source_span: '14:25'
source_sha256: 7fb9c3240b2efe4e27bdc4dccb0d79683cf19802d68b34386612301ccafb5bb1
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.section_doc_contribution:sync_doc_shard;
  contract-sha256:e28cae7e9fcd38afb85cf5e032f089bcbf38627d932a36978ac5d1ebcae33efc
---

# sync_doc_shard

## Signature

sync_doc_shard(store_path, doc, d_path, m_entry, report, process_doc_sections)

## Docstring

This document's sections shard, current: reused untouched when its `source_hash` already
matches what the shard on disk carries, (re)parsed and (re)written otherwise.
`process_doc_sections` is section_rebuild's own parser, passed in rather than imported
back (this module is the one section_rebuild imports).

## Imports

["__future__", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.models", "sldb.store.section_paths"]

## Purpose

Not documented.

## Architecture

Not documented.
