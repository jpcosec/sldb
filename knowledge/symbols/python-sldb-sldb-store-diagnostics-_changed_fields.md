---
id: python-sldb-sldb-store-diagnostics-_changed_fields
system: sldb
module: sldb.store.diagnostics
qualname: _changed_fields
kind: FunctionDef
source_path: sldb/store/diagnostics.py
source_span: 69:78
source_sha256: 8df97842ce8ae42fe7bd7d412973d2a760e684bbcde8e00f0b22146d56f8bab7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.diagnostics:_changed_fields; contract-sha256:7e701452c28ca585a2507317f1ea83075fdae513b8b64f5c04106cbed2923e66
---

# _changed_fields

## Signature

_changed_fields(in_index: dict[str, str], on_disk: dict[str, str])

## Docstring

The field names whose hashes disagree, plus those present on only one side.

Empty when either side has no map: a store written before `field_hashes` cannot be asked
which field moved, and saying "none" there would read as "nothing changed" when
`content_hash` already said otherwise.

## Imports

["__future__", "pathlib", "sldb.store.diagnostics_models", "sldb.store.diagnostics_models.text_history", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.legacy_contract", "sldb.store.model_node", "sldb.store.model_origin", "sldb.store.models", "typing"]

## Purpose

The field names whose hashes disagree, plus those present on only one side.

## Architecture

Not documented.
