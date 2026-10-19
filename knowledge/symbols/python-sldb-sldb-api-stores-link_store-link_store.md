---
id: python-sldb-sldb-api-stores-link_store-link_store
system: sldb
module: sldb.api.stores.link_store
qualname: link_store
kind: FunctionDef
source_path: sldb/api/stores/link_store.py
source_span: '19:44'
source_sha256: 31f9f05aeb9367a543f24fd7216c3df5745de95d2deacd34a4a3fefe7672206d
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.link_store:link_store; contract-sha256:0e9b8db7aec8a925adc416f9254d7f4d2e05f6a4585dc3e417f00f7617a7cedc
---

# link_store

## Signature

link_store(store: str | Path | None, other_store: str | Path, name: str | None=None, replace: bool=False)

## Docstring

Record another store as linked into `store`.

Args:
    store: The linking store (path, alias, or None to discover it).
    other_store: Path of the `.sldb` directory to link.
    name: Alias for the link; defaults to the name of the directory holding `other_store`.
    replace: Point a link already recorded under that name at `other_store` instead.

Returns:
    The link as recorded in the store index.

Raises:
    SLDBStoreError: When `other_store` is not a store or is the linking store itself, or
        the name is invalid, reserved (`local`) or already linked (and not `replace`).

## Imports

["__future__", "os", "pathlib", "sldb.api.stores.doc_ref", "sldb.api.stores.linked_store", "sldb.api.stores.open_store", "sldb.api.stores.unlink_store", "sldb.core.exceptions", "sldb.store.io", "sldb.store.layout", "sldb.store.models.store_entry", "sldb.store.models.store_index"]

## Purpose

Record another store as linked into `store`.

## Architecture

Not documented.
