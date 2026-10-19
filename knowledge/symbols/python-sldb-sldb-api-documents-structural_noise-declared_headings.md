---
id: python-sldb-sldb-api-documents-structural_noise-declared_headings
system: sldb
module: sldb.api.documents.structural_noise
qualname: declared_headings
kind: FunctionDef
source_path: sldb/api/documents/structural_noise.py
source_span: '14:28'
source_sha256: 1f7a37afefc55f4924aed85f6460cad1659f547025f798d68f9c1a37acc3a711
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.structural_noise:declared_headings;
  contract-sha256:1c5f6e4f148a4790fc0c6ef24cbbe3127b103e6e555064f1dc56d80650a397bf
---

# declared_headings

## Signature

declared_headings(template: str)

## Docstring

The literal heading slots a template declares, and the levels it leaves open.

Args:
    template: A model's `__template__`.

Returns:
    `(literals, wildcard_levels)`; a heading whose title is a marker (`⸢rev•title⸥`)
    declares its whole level open, since the rendered title comes from a field.

## Imports

["__future__", "sldb.api.documents.heading_scan", "sldb.api.documents.structural_noise_report"]

## Purpose

The literal heading slots a template declares, and the levels it leaves open.

## Architecture

Not documented.
