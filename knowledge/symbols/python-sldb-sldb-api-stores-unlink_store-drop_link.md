---
id: python-sldb-sldb-api-stores-unlink_store-drop_link
system: sldb
module: sldb.api.stores.unlink_store
qualname: drop_link
kind: FunctionDef
source_path: sldb/api/stores/unlink_store.py
source_span: '39:47'
source_sha256: cc89416a37d58ae0fedd3f05660605349181c2156c9cad79c822926b6a9441ca
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.unlink_store:drop_link; contract-sha256:1651b08dfff527a0391fb88b67e220f55e2ce133491f92fb1faf7789409bd18e
---

# drop_link

## Signature

drop_link(sp: Path, name: str)

## Docstring

Remove the entry `name` from the store index; refused when there is none.

## Imports

["__future__", "pathlib", "sldb.api.stores.linked_store", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io"]

## Purpose

Remove the entry `name` from the store index; refused when there is none.

## Architecture

Not documented.
