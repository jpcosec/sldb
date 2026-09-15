---
id: python-sldb-sldb-sldb-store-io-_save_if_changed
system: sldb
module: sldb.sldb.store.io
qualname: _save_if_changed
kind: FunctionDef
source_path: sldb/store/io/__init__.py
source_span: 59:68
source_sha256: 0b240d527fd6f837d606be3dad180b7b89529226c9a8bf5a3d4666ecde28097f
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.store.io:_save_if_changed; contract-sha256:47301b7e4d04289ada1ab0c8048f9e67d8aa9edd8d7f7d86762d2264a7780d3f
---

# _save_if_changed

## Signature

_save_if_changed(path: Path, index, saver)

## Docstring

Write only when the content differs from what the file already holds: a rebuild that
changes nothing leaves the file, its mtime and every cache keyed on it alone.

## Imports

["pathlib", "sldb.store.io.documents_index", "sldb.store.io.lock", "sldb.store.io.models_index", "sldb.store.io.sections_index", "sldb.store.io.semantic_dag", "sldb.store.io.semantic_index", "sldb.store.io.store_index", "sldb.store.layout", "sldb.store.models"]

## Purpose

Not documented.

## Architecture

Not documented.
