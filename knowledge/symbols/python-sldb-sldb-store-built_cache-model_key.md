---
id: python-sldb-sldb-store-built_cache-model_key
system: sldb
module: sldb.store.built_cache
qualname: model_key
kind: FunctionDef
source_path: sldb/store/built_cache.py
source_span: '32:38'
source_sha256: 84323b24a21fe928a344e41512249a0da6444efd6a7b553701d8aadebbdc2bd0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.built_cache:model_key; contract-sha256:5712eb3a6c4b7bd2105ccf3950c9fa62f0766a86c3ef291f0248992307e6f770
---

# model_key

## Signature

model_key(m_idx: Any)

## Docstring

model_hash plus what the models index records about the class: version and semantics.

The node, not the roster: a derived result built under one contract must not be reused
under another, and the contract is exactly what the roster alone cannot see.

## Imports

["__future__", "json", "pathlib", "sldb.store", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
