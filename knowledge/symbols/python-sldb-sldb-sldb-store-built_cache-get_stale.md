---
id: python-sldb-sldb-sldb-store-built_cache-get_stale
system: sldb
module: sldb.sldb.store.built_cache
qualname: get_stale
kind: FunctionDef
source_path: sldb/store/built_cache.py
source_span: '46:51'
source_sha256: 84323b24a21fe928a344e41512249a0da6444efd6a7b553701d8aadebbdc2bd0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.built_cache:get_stale; contract-sha256:b893306c12a6836985ee881b4b8ea8da63243ee9817f8ef82325aa6bcba973f6
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

Not documented.

## Architecture

Not documented.
