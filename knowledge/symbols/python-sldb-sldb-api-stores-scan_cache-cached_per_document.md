---
id: python-sldb-sldb-api-stores-scan_cache-cached_per_document
system: sldb
module: sldb.api.stores.scan_cache
qualname: cached_per_document
kind: FunctionDef
source_path: sldb/api/stores/scan_cache.py
source_span: '20:26'
source_sha256: 47bf32df1a4dd2ed835bd4d31553b59c252c64fb20beee459b936692d9491437
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.scan_cache:cached_per_document; contract-sha256:34da09f246cf77733cdd3444d6e6afb498002bb9b5f2b97727f7bd694ab3c023
---

# cached_per_document

## Signature

cached_per_document(store_path: Path, kind: str, docs: list[tuple[Any, str]], compute: Callable[[Any, str], Any])

## Docstring

`(doc, result)` for each `(doc, text)`: the stored result when its key still holds.

## Imports

["__future__", "hashlib", "json", "pathlib", "typing"]

## Purpose

`(doc, result)` for each `(doc, text)`: the stored result when its key still holds.

## Architecture

Not documented.
