---
id: python-sldb-sldb-api-stores-index_refresh-_restamp
system: sldb
module: sldb.api.stores.index_refresh
qualname: _restamp
kind: FunctionDef
source_path: sldb/api/stores/index_refresh.py
source_span: 102:112
source_sha256: 52ff82f50024af90f44606255ea3e419ec7c3bf6b714754debcb1a825838e1fc
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.index_refresh:_restamp; contract-sha256:a86bf68776af04817ee5eb0dcdc4d51f8670acd45d38673304c608288c7c82cd
---

# _restamp

## Signature

_restamp(doc: Any, mtype: Any, m_name: str, text: str, fresh: str, force: bool)

## Docstring

Re-extract and store the hashes; False when they came back identical (nothing moved).

`doc.source_hash` is updated before extracting on purpose: the extraction cache is keyed
on the source hash the payload belongs to, so passing the old one here would read another
document's cached payload (the file's previous content) and sign a wrong content_hash.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.document_field_hashes", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "typing"]

## Purpose

Re-extract and store the hashes; False when they came back identical (nothing moved).

## Architecture

Not documented.
