---
id: python-sldb-sldb-api-model_registry-federated_lookup-_build_federated_entry
system: sldb
module: sldb.api.model_registry.federated_lookup
qualname: _build_federated_entry
kind: FunctionDef
source_path: sldb/api/model_registry/federated_lookup.py
source_span: '54:59'
source_sha256: ce5d7d76fd7183cd7e3bfdfbb914ac88893dae60f2be2cc42a4ec5d20c3f7609
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.federated_lookup:_build_federated_entry;
  contract-sha256:10f5449730f9eac7d4b72d6aa5a33e187cf06153a9e3622012fe8648d6afe402
---

# _build_federated_entry

## Signature

_build_federated_entry(destination_store: Path, linked_store: Path, remote_entry: Any, pythonpath: str | None, store_alias: str | None=None)

## Docstring

Import the remote model from where its owner lives and register it here as inherited.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.federated_registration", "sldb.api.model_registry.model_reference", "sldb.store.io", "sldb.store.layout", "sldb.store.resolver", "typing"]

## Purpose

Import the remote model from where its owner lives and register it here as inherited.

## Architecture

Not documented.
