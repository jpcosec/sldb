---
id: python-sldb-sldb-sldb-api-search-search
system: sldb
module: sldb.sldb.api.search
qualname: search
kind: FunctionDef
source_path: sldb/api/search.py
source_span: '26:48'
source_sha256: 649bd8c09783e097809c4128dbde151bbf85baa580d83d71a452051ccf22b089
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.search:search; contract-sha256:d522845533d239f76f869d721407f99a134033b0bef3911dbefb87ecfcdf353e
---

# search

## Signature

search(store_path: Path, term: str, search_in: str='both', kinds: set[str] | None=None, where: str | None=None, select: str | None=None, limit: int | None=None, pythonpath: str | None=None, regex: bool=False, fuzzy: bool=False, include_linked: bool=False)

## Docstring

Match records exactly as `sldb find` matches, serialized as its JSON results.

## Imports

["__future__", "pathlib", "sldb.api.records", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
