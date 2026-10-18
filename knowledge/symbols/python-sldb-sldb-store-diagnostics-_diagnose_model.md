---
id: python-sldb-sldb-store-diagnostics-_diagnose_model
system: sldb
module: sldb.store.diagnostics
qualname: _diagnose_model
kind: FunctionDef
source_path: sldb/store/diagnostics.py
source_span: 98:109
source_sha256: 8df97842ce8ae42fe7bd7d412973d2a760e684bbcde8e00f0b22146d56f8bab7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.diagnostics:_diagnose_model; contract-sha256:4858b62f43e81a7ae2d71a36e797eebdc5c15a4c2f7d53f05ab5b9cb99afc96b
---

# _diagnose_model

## Signature

_diagnose_model(model_entry, root, pythonpath, resolve_model_ref: Callable)

## Docstring

The model node, split into the two children that can move it: its document roster and
its contract. Attributing the node to one of them is the whole point of storing both.

## Imports

["__future__", "pathlib", "sldb.store.diagnostics_models", "sldb.store.diagnostics_models.text_history", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.legacy_contract", "sldb.store.model_node", "sldb.store.model_origin", "sldb.store.models", "typing"]

## Purpose

The model node, split into the two children that can move it: its document roster and its contract. Attributing the node to one of them is the whole point of storing both.

## Architecture

Not documented.
