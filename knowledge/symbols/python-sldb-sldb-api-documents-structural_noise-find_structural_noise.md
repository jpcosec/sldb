---
id: python-sldb-sldb-api-documents-structural_noise-find_structural_noise
system: sldb
module: sldb.api.documents.structural_noise
qualname: find_structural_noise
kind: FunctionDef
source_path: sldb/api/documents/structural_noise.py
source_span: '31:45'
source_sha256: 1f7a37afefc55f4924aed85f6460cad1659f547025f798d68f9c1a37acc3a711
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.structural_noise:find_structural_noise;
  contract-sha256:8eda6608b4fd40e9a10dfc4d880b7b92b7e0799d990d3d2fa31bcd12c41f5e4a
---

# find_structural_noise

## Signature

find_structural_noise(model_type: type, markdown: str, name: str='')

## Docstring

The document's headings that the model does not declare.

Args:
    model_type: The `StructuredNLDoc` subclass the document is tracked as.
    markdown: The document's Markdown source.
    name: Document name, used only in the error message.

Returns:
    A report; `report.clean` is True when every heading is declared.

## Imports

["__future__", "sldb.api.documents.heading_scan", "sldb.api.documents.structural_noise_report"]

## Purpose

Not documented.

## Architecture

Not documented.
