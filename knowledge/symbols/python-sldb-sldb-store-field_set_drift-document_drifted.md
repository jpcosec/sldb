---
id: python-sldb-sldb-store-field_set_drift-document_drifted
system: sldb
module: sldb.store.field_set_drift
qualname: document_drifted
kind: FunctionDef
source_path: sldb/store/field_set_drift.py
source_span: '35:44'
source_sha256: 1ad57505444177e11663cbe39b1fbccceff24a84e0316e440362a7ded430dca4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.field_set_drift:document_drifted; contract-sha256:e23a88cc191c3d14760cddf45b78bcedc35f24f8d0a25ac8ab3d4079a5295af3
---

# document_drifted

## Signature

document_drifted(doc: Any, root: Path, model_type: Any)

## Docstring

Whether a tracked document was signed under another field set. Only a document whose map
names an undeclared field is re-extracted, to tell an `extra="allow"` key it still yields
from one the current class no longer produces.

## Imports

["__future__", "pathlib", "sldb.store.hashing", "typing"]

## Purpose

Whether a tracked document was signed under another field set. Only a document whose map names an undeclared field is re-extracted, to tell an `extra="allow"` key it still yields from one the current class no longer produces.

## Architecture

Not documented.
