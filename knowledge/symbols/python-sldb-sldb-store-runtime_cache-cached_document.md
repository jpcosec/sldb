---
id: python-sldb-sldb-store-runtime_cache-cached_document
system: sldb
module: sldb.store.runtime_cache
qualname: cached_document
kind: FunctionDef
source_path: sldb/store/runtime_cache.py
source_span: 49:61
source_sha256: 870a33b2e031d380c875372e22bbf508b533af2cbd6dae4f59d6ddb6e563db78
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.runtime_cache:cached_document; contract-sha256:4995c17af03d58ad71597cc0b4147369f6af7b68669cc93b948d651ca861277b
---

# cached_document

## Signature

cached_document(entry: Any, root: Path, s_path: Path, s_name: str, m_name: str, model_type: type, loader: Callable[[], Any])

## Docstring

One document by its store, its leaf: (path, source_hash[, mtime, size]), and the contract
of the class being extracted with, so a moved contract invalidates the entry (in memory and
on disk) even when the leaf did not. The contract is hashed from `model_type` itself, not
read from the models index: the index only learns of a contract change when something
writes, and a pure read (new field on the class, same Markdown) must not be served a payload
extracted under the old contract — the standing bug where a new field stayed invisible.

## Imports

["__future__", "dataclasses", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.runtime_cache_signature", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
