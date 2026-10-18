---
id: python-sldb-sldb-api-documents-refuse_structural_noise-refuse_structural_noise
system: sldb
module: sldb.api.documents.refuse_structural_noise
qualname: refuse_structural_noise
kind: FunctionDef
source_path: sldb/api/documents/refuse_structural_noise.py
source_span: '13:28'
source_sha256: 73abefa039324b40280500fda3c6a69e92a6aad7de66946c88e6d57fd19bf6e7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.refuse_structural_noise:refuse_structural_noise;
  contract-sha256:0ec4a61fbc2c990ffff8974b6c8fcd2c89ccc2cb00f705775de8973c211c81a0
---

# refuse_structural_noise

## Signature

refuse_structural_noise(model_type: type, markdown: str, name: str)

## Docstring

Raise unless every heading in `markdown` is declared by the model's template.

Args:
    model_type: The `StructuredNLDoc` subclass the document is tracked as.
    markdown: The document's Markdown source.
    name: Document name, used in the message.

Raises:
    SLDBValidationError: When the document carries undeclared headings; the message
        names them and points at a child model declaring them as `optrev` fields.

## Imports

["__future__", "sldb.api.documents.structural_noise", "sldb.core.exceptions"]

## Purpose

Raise unless every heading in `markdown` is declared by the model's template.

## Architecture

Not documented.
