---
id: python-sldb-sldb-api-stores-document_field_hashes-_extracted_payload
system: sldb
module: sldb.api.stores.document_field_hashes
qualname: _extracted_payload
kind: FunctionDef
source_path: sldb/api/stores/document_field_hashes.py
source_span: '14:23'
source_sha256: ead488d6aebfdbeb29692f6465bee59ec6145f1766a0b15b767f7841d27f6952
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.document_field_hashes:_extracted_payload;
  contract-sha256:7014cea70cc9c22d8d891ac37420e62b8f03a5f9de19695ae224e7ef67b1c402
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

The document's payload, from the runtime cache when it can be trusted.

## Architecture

Not documented.
