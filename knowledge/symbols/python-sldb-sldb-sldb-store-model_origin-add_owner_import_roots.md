---
id: python-sldb-sldb-sldb-store-model_origin-add_owner_import_roots
system: sldb
module: sldb.sldb.store.model_origin
qualname: add_owner_import_roots
kind: FunctionDef
source_path: sldb/store/model_origin.py
source_span: '53:58'
source_sha256: 50c763d3d5219d878aa05edd93543ec59204335bd82b37fa28b50be71676f29e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.model_origin:add_owner_import_roots;
  contract-sha256:e572942736fe90990f2c17146def2f014bce924f703d610cb4526f9b904b36a4
---

# add_owner_import_roots

## Signature

add_owner_import_roots(store_path: Path)

## Docstring

Put the owners' project roots on `sys.path`, once each, so inherited models import
without a `--pythonpath`; a path given explicitly is inserted in front of them later.

## Imports

["__future__", "pathlib", "sldb.store.io", "sldb.store.layout", "sys", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
