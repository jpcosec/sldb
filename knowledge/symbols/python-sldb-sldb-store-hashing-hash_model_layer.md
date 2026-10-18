---
id: python-sldb-sldb-store-hashing-hash_model_layer
system: sldb
module: sldb.store.hashing
qualname: hash_model_layer
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: 106:112
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.hashing:hash_model_layer; contract-sha256:ca3d309a43e2fed266c6b2c92d222be35d1cc784dd828d9858f2890ac2d0cad0
---

# hash_model_layer

## Signature

hash_model_layer(roster_hash: str, contract_hash: str)

## Docstring

A model node from its two children: the document roster and the model's contract.

Both are persisted next to it (`ModelsIndex.roster_hash`/`contract_hash`) so a node that
disagrees can be attributed to one child instead of reported as a bare mismatch.

## Imports

["hashlib", "json", "sldb.store.codec", "sldb.store.models", "sldb.store.semantic_tags", "typing"]

## Purpose

A model node from its two children: the document roster and the model's contract.

## Architecture

Not documented.
