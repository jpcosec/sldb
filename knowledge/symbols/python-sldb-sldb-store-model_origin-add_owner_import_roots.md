---
id: python-sldb-sldb-store-model_origin-add_owner_import_roots
system: sldb
module: sldb.store.model_origin
qualname: add_owner_import_roots
kind: FunctionDef
source_path: sldb/store/model_origin.py
source_span: '53:58'
source_sha256: 50c763d3d5219d878aa05edd93543ec59204335bd82b37fa28b50be71676f29e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.model_origin:add_owner_import_roots; contract-sha256:b389abbc860a04fbd5b3219c66f59b54e0b1d5b77aa2b7206c7d7d9b6b4d961b
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

Put the owners' project roots on `sys.path`, once each, so inherited models import without a `--pythonpath`; a path given explicitly is inserted in front of them later.

## Architecture

Not documented.
