---
id: python-sldb-sldb-store-edge_index-validation-_effective_types
system: sldb
module: sldb.store.edge_index.validation
qualname: _effective_types
kind: FunctionDef
source_path: sldb/store/edge_index/validation.py
source_span: 60:64
source_sha256: 03c609667a78e9116e3dc13b69649e8b0aa72d0690774488e6c79d05d6c9d81e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.validation:_effective_types; contract-sha256:706ea0d37cddca8670011d58907a30b0d95d0ac6e55f8e4a5b28617323c7ae3a
---

# _effective_types

## Signature

_effective_types(tracked: dict[str, dict[str, Any]])

## Docstring

The types a derived edge is checked against once the store ran `edges init`: sldb's own
definition of a builtin wins, since sldb produces those edges. A store may author a type
under a builtin's name (selfdoc's code `contains`); it applies to authored edges only.

## Imports

["__future__", "collections", "sldb.store.edge_index.edge_index", "sldb.store.edge_index.resolve", "sldb.store.model_contract", "sldb.store.models", "typing"]

## Purpose

The types a derived edge is checked against once the store ran `edges init`: sldb's own definition of a builtin wins, since sldb produces those edges. A store may author a type under a builtin's name (selfdoc's code `contains`); it applies to authored edges only.

## Architecture

Not documented.
