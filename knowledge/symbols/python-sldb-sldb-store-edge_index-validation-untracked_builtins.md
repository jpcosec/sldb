---
id: python-sldb-sldb-store-edge_index-validation-untracked_builtins
system: sldb
module: sldb.store.edge_index.validation
qualname: untracked_builtins
kind: FunctionDef
source_path: sldb/store/edge_index/validation.py
source_span: '52:57'
source_sha256: 03c609667a78e9116e3dc13b69649e8b0aa72d0690774488e6c79d05d6c9d81e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.validation:untracked_builtins;
  contract-sha256:60f5e9b7e84d9b474fd6ca8199df1a7aa65509abd6c80fc8ba70f4d8f9e5dc0e
---

# untracked_builtins

## Signature

untracked_builtins(index: EdgeIndex)

## Docstring

Builtin types newer than the store's `edges init` that its derived edges use (re-run init to track them).

## Imports

["__future__", "collections", "sldb.store.edge_index.edge_index", "sldb.store.edge_index.resolve", "sldb.store.model_contract", "sldb.store.models", "typing"]

## Purpose

Builtin types newer than the store's `edges init` that its derived edges use (re-run init to track them).

## Architecture

Not documented.
