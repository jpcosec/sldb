---
id: python-sldb-sldb-sldb-api-stores-link_store-record_store_link
system: sldb
module: sldb.sldb.api.stores.link_store
qualname: record_store_link
kind: FunctionDef
source_path: sldb/api/stores/link_store.py
source_span: 71:92
source_sha256: 31f9f05aeb9367a543f24fd7216c3df5745de95d2deacd34a4a3fefe7672206d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.link_store:record_store_link; contract-sha256:0b0b7d3e95d614b8262fae02cf729f45c1595cb09ee976dec7e8593c37ca28dc
---

# record_store_link

## Signature

record_store_link(sp: Path, root: Path, other: Path, name: str)

## Docstring

Append a link entry to the store index without checking that `other` exists.

Args:
    sp: The linking store's `.sldb` directory.
    root: The linking store's project root.
    other: Resolved `.sldb` directory being linked.
    name: Alias for the link.

Returns:
    The path recorded for the link, always relative to `root` so the link survives a
    checkout of both repos at another location.

Raises:
    SLDBStoreError: When the name is already linked.

## Imports

["__future__", "os", "pathlib", "sldb.api.stores.doc_ref", "sldb.api.stores.linked_store", "sldb.api.stores.open_store", "sldb.api.stores.unlink_store", "sldb.core.exceptions", "sldb.store.io", "sldb.store.layout", "sldb.store.models.store_entry", "sldb.store.models.store_index"]

## Purpose

Not documented.

## Architecture

Not documented.
