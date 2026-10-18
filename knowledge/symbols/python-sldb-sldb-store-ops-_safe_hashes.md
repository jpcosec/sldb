---
id: python-sldb-sldb-store-ops-_safe_hashes
system: sldb
module: sldb.store.ops
qualname: _safe_hashes
kind: FunctionDef
source_path: sldb/store/ops.py
source_span: 83:92
source_sha256: 15a1ed96fccad244114a03a10e83846e3c5596b9f5fb9a59a08be3e7211c7e26
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.ops:_safe_hashes; contract-sha256:593478227b34dea555313a851f05416ab649c19dd9ed1233c01d800a43b012d7
---

# _safe_hashes

## Signature

_safe_hashes(model_type: type, text: str)

## Docstring

A document's `content_hash` and per-field map, or empties when it no longer extracts.

An empty map means "could not be computed", never "no fields": a consumer comparing
against it has to fall back to the whole document.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models", "sldb.store.section_rebuild", "sldb.store.semantic", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
