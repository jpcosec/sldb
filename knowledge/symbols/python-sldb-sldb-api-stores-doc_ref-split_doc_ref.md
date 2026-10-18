---
id: python-sldb-sldb-api-stores-doc_ref-split_doc_ref
system: sldb
module: sldb.api.stores.doc_ref
qualname: split_doc_ref
kind: FunctionDef
source_path: sldb/api/stores/doc_ref.py
source_span: '28:40'
source_sha256: a6dd4ac0b0447e39d616a1c5f419dd323befc16e9b56d74bc736fc0618e1c1ab
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.doc_ref:split_doc_ref; contract-sha256:c9d3ed6c1c7ae87c822d09b1bd919e6cfd7869e38b235ff63f3e6733c5981567
---

# split_doc_ref

## Signature

split_doc_ref(store_path: Path, ref: str)

## Docstring

(link alias, reference inside that store); the alias is None for the local store.

Args:
    store_path: The store the reference is read from; its links give prefixes meaning.
    ref: `name`, `Model/name`, a tracked path, or any of those behind `alias:`.

## Imports

["__future__", "pathlib", "re", "sldb.api.stores.store_links"]

## Purpose

Not documented.

## Architecture

Not documented.
