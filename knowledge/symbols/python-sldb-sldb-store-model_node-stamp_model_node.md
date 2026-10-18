---
id: python-sldb-sldb-store-model_node-stamp_model_node
system: sldb
module: sldb.store.model_node
qualname: stamp_model_node
kind: FunctionDef
source_path: sldb/store/model_node.py
source_span: '17:30'
source_sha256: d422f8f78c044d5bfe5d2dae5989d24570419029ca139b2797474e6da0defbb4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.model_node:stamp_model_node; contract-sha256:736444ac231e3f714ac530ad35e0bace6b57e7921d47b25eddc99f9ca1eabfd2
---

# stamp_model_node

## Signature

stamp_model_node(m_idx: Any, roster_hash: str, model_type: Any | None, entry: Any | None=None)

## Docstring

Record this model's roster, its contract and the node the two make up.

`model_type` is None when the class cannot be imported (a broken or federated model): the
contract already recorded is kept rather than being blanked, so an unimportable model does
not report its contract as having changed. `entry`, the model's line in the store index,
gets the family too: both record it.

## Imports

["__future__", "sldb.store.hashing", "typing"]

## Purpose

Record this model's roster, its contract and the node the two make up.

## Architecture

Not documented.
