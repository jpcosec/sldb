---
id: python-sldb-sldb-api-model_registry-remove_model-remove_model
system: sldb
module: sldb.api.model_registry.remove_model
qualname: remove_model
kind: FunctionDef
source_path: sldb/api/model_registry/remove_model.py
source_span: '21:46'
source_sha256: c74f8174a85521bc8296eee2045d247a2369edd3c5531240a6360569f2461436
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.remove_model:remove_model; contract-sha256:9bda2ce9992675dcffb200b743ebd2fab873a16d13e6ba25ada5a0201f64ca2a
---

# remove_model

## Signature

remove_model(store: str | Path | None, model_name: str, pythonpath: str | None=None, actor: str | None=None, untrack_documents: bool=False)

## Docstring

Unregister a model: its entry, indexes and shards go; its class is never imported.

Args:
    store: The store (path, alias, or None to discover it).
    model_name: The registered model's name.
    pythonpath: Directory to import the remaining models from (derived indexes are rebuilt).
    actor: Optional label recorded in the store journal for this write.
    untrack_documents: Also stop tracking its documents (their Markdown files stay), the
        way to drop a model whose class was deleted while documents were tracked.

Returns:
    The registry record that was removed.

Raises:
    SLDBModelError: The model is not registered, or still tracks documents and
        `untrack_documents` is False.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_registry.model_files", "sldb.api.model_registry.model_reference", "sldb.api.model_registry.model_registration", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.io", "sldb.store.io.rollback", "sldb.store.layout", "sldb.store.ops"]

## Purpose

Unregister a model: its entry, indexes and shards go; its class is never imported.

## Architecture

Not documented.
