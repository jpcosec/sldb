---
id: python-sldb-sldb-sldb-store-hashing-hash_model_layer
system: sldb
module: sldb.sldb.store.hashing
qualname: hash_model_layer
kind: FunctionDef
source_path: sldb/store/hashing.py
source_span: 106:112
source_sha256: 307e4065fa6890503d585512c64bf412c3d1ecb617f5cbf575d9d1bd97c24b7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.hashing:hash_model_layer; contract-sha256:697ae236324f70c427ab2c2d1f943197c63f645bbe9515dadf3a47b65cbcdafa
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

Not documented.

## Architecture

Not documented.
