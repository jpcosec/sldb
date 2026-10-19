---
id: python-sldb-sldb-store-model_node-_declared_family
system: sldb
module: sldb.store.model_node
qualname: _declared_family
kind: FunctionDef
source_path: sldb/store/model_node.py
source_span: '33:38'
source_sha256: d422f8f78c044d5bfe5d2dae5989d24570419029ca139b2797474e6da0defbb4
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.model_node:_declared_family; contract-sha256:ef9a09cfa8ad18caac4cd53c3bbbbf9859bf826c8108cf68663795207e1e3894
---

# _declared_family

## Signature

_declared_family(model_type: Any)

## Docstring

The class's `__family__` as it is now: it used to be read only at `models add`, so a
family changed in the class never reached the store (AgentsKBs, 2026-10-03).

## Imports

["__future__", "sldb.store.hashing", "typing"]

## Purpose

The class's `__family__` as it is now: it used to be read only at `models add`, so a family changed in the class never reached the store (AgentsKBs, 2026-10-03).

## Architecture

Not documented.
