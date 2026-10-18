---
id: python-sldb-sldb-sldb-api-stores-store_links-store_links
system: sldb
module: sldb.sldb.api.stores.store_links
qualname: store_links
kind: FunctionDef
source_path: sldb/api/stores/store_links.py
source_span: '15:28'
source_sha256: 44b989ceeb32dc4b0b19efa9c811e36837361f265beea57dd837b9ac53c30084
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.store_links:store_links; contract-sha256:b3e8edc1a83e039f16ea428661649765b3afa0f948b9353ab36f1f49cc0136a8
---

# store_links

## Signature

store_links(store_path: Path)

## Docstring

Every direct link of the store, sorted by name.

Args:
    store_path: The linking store's `.sldb` directory.

Returns:
    One `{name, path, resolved, status}` per link: `path` as recorded, `resolved` the
    absolute `.sldb` it points to, `status` one of `ok`, `missing` (no directory there)
    or `not-a-store` (a directory that holds no store).

## Imports

["__future__", "pathlib", "sldb.store.io", "sldb.store.layout"]

## Purpose

Not documented.

## Architecture

Not documented.
