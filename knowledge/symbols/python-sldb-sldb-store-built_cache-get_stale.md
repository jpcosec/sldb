---
id: python-sldb-sldb-store-built_cache-get_stale
system: sldb
module: sldb.store.built_cache
qualname: get_stale
kind: FunctionDef
source_path: sldb/store/built_cache.py
source_span: '46:51'
source_sha256: 84323b24a21fe928a344e41512249a0da6444efd6a7b553701d8aadebbdc2bd0
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.built_cache:get_stale; contract-sha256:19954747db9268c0ebc9b0660551d6e5a228c56cf39060a9cc4ab774f3c27e06
---

# get_stale

## Signature

get_stale(s_path: Path, kind: str, model: str)

## Docstring

The last value cached for `model`, regardless of whether its key still matches: a
rebuild whose key moved (a source_hash change moved the model's roster_hash) still finds
here the per-document work it does not need to redo (PLAN 15 M2).

## Imports

["__future__", "json", "pathlib", "sldb.store", "typing"]

## Purpose

The last value cached for `model`, regardless of whether its key still matches: a rebuild whose key moved (a source_hash change moved the model's roster_hash) still finds here the per-document work it does not need to redo (PLAN 15 M2).

## Architecture

Not documented.
