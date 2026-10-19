---
id: python-sldb-sldb-api-stores-store_links-store_links
system: sldb
module: sldb.api.stores.store_links
qualname: store_links
kind: FunctionDef
source_path: sldb/api/stores/store_links.py
source_span: '15:28'
source_sha256: 44b989ceeb32dc4b0b19efa9c811e36837361f265beea57dd837b9ac53c30084
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.store_links:store_links; contract-sha256:e71282d722ebead321e2219bddc17fd4e573ca295e8a86118f24855e930bde11
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

Every direct link of the store, sorted by name.

## Architecture

Not documented.
