---
id: python-sldb-sldb-store-io-_save_if_changed
system: sldb
module: sldb.store.io
qualname: _save_if_changed
kind: FunctionDef
source_path: sldb/store/io/__init__.py
source_span: 67:76
source_sha256: a65d487517f80e48a31662a55b977d5d2a86eaaa5f6dc2379c796c8b06ddfee0
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.io:_save_if_changed; contract-sha256:20870b3589ca625c946481d9befcf769b63b5d7c7f3253ef7cb693da957fec14
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

Write only when the content differs from what the file already holds: a rebuild that changes nothing leaves the file, its mtime and every cache keyed on it alone.

## Architecture

Not documented.
