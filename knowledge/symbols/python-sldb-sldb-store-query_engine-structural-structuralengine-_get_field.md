---
id: python-sldb-sldb-store-query_engine-structural-structuralengine-_get_field
system: sldb
module: sldb.store.query_engine.structural
qualname: StructuralEngine._get_field
kind: FunctionDef
source_path: sldb/store/query_engine/structural.py
source_span: 79:87
source_sha256: 31245e018b0342ac6d01f2ab18a93752e26e28faea8b9379bf2021ebcfd4d5d9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.query_engine.structural:StructuralEngine._get_field;
  contract-sha256:9e44685b90ada0954a25cfae52c3576fc2550a9ae3dbce51033132d25ee11fe2
---

# StructuralEngine._get_field

## Signature

_get_field(cls, target, field_name: str)

## Docstring

Walk a dotted field path: keys into dict subfields, integers into list items
(`tasks.0.title`). Same traversal as `fields show docs/<doc>/tasks/0/title`.

## Imports

["__future__", "pathlib", "re", "sldb.store.io", "typing"]

## Purpose

Walk a dotted field path: keys into dict subfields, integers into list items (`tasks.0.title`). Same traversal as `fields show docs/<doc>/tasks/0/title`.

## Architecture

Not documented.
