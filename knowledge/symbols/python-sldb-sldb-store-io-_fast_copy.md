---
id: python-sldb-sldb-store-io-_fast_copy
system: sldb
module: sldb.store.io
qualname: _fast_copy
kind: FunctionDef
source_path: sldb/store/io/__init__.py
source_span: '34:39'
source_sha256: a65d487517f80e48a31662a55b977d5d2a86eaaa5f6dc2379c796c8b06ddfee0
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.io:_fast_copy; contract-sha256:e3f258f22748cca71cdc98a8efe5fe3311d3ce25cf67b9dca049682feed549a1
---

# _fast_copy

## Signature

_fast_copy(index)

## Docstring

An independent copy of a parsed index, cheaper than `model_copy(deep=True)`: pydantic's
own dump/validate round-trip instead of the generic recursive `copy.deepcopy` it uses
internally (PLAN 15 M2) — ~4x faster on a realistic SectionsIndex in this codebase's own
measurements, and every caller through `_cached` already only reads validated data back.

## Imports

["pathlib", "sldb.store.io.documents_index", "sldb.store.io.lock", "sldb.store.io.models_index", "sldb.store.io.sections_index", "sldb.store.io.semantic_dag", "sldb.store.io.semantic_index", "sldb.store.io.store_index", "sldb.store.layout", "sldb.store.models"]

## Purpose

An independent copy of a parsed index, cheaper than `model_copy(deep=True)`: pydantic's own dump/validate round-trip instead of the generic recursive `copy.deepcopy` it uses internally (PLAN 15 M2) — ~4x faster on a realistic SectionsIndex in this codebase's own measurements, and every caller through `_cached` already only reads validated data back.

## Architecture

Not documented.
