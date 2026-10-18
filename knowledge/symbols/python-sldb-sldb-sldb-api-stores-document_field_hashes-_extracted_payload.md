---
id: python-sldb-sldb-sldb-api-stores-document_field_hashes-_extracted_payload
system: sldb
module: sldb.sldb.api.stores.document_field_hashes
qualname: _extracted_payload
kind: FunctionDef
source_path: sldb/api/stores/document_field_hashes.py
source_span: '14:23'
source_sha256: ead488d6aebfdbeb29692f6465bee59ec6145f1766a0b15b767f7841d27f6952
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.document_field_hashes:_extracted_payload;
  contract-sha256:7c85d1a553cec5e370603a28dd52ffaf8a4ad893c8daa9feb2fd36ad56b45d29
---

# _extracted_payload

## Signature

_extracted_payload(mtype: Any, doc: Any, text: str, force: bool)

## Docstring

The document's payload, from the runtime cache when it can be trusted.

The cached payload is skipped when the contract moved: it was extracted under the previous
contract, which is exactly what must not win here.

## Imports

["__future__", "sldb.store.hashing", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
