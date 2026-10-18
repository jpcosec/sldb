---
id: python-sldb-sldb-sldb-api-documents-refuse_structural_noise-refuse_structural_noise
system: sldb
module: sldb.sldb.api.documents.refuse_structural_noise
qualname: refuse_structural_noise
kind: FunctionDef
source_path: sldb/api/documents/refuse_structural_noise.py
source_span: '13:28'
source_sha256: 73abefa039324b40280500fda3c6a69e92a6aad7de66946c88e6d57fd19bf6e7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.refuse_structural_noise:refuse_structural_noise;
  contract-sha256:f4e489bc0e5c320a9fe496915f18eb91950a31089621d3b0f5c0f5ebc6200a0b
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

Not documented.

## Architecture

Not documented.
