---
id: python-sldb-sldb-selfdoc-planned_document-planneddocument
system: sldb
module: sldb.selfdoc.planned_document
qualname: PlannedDocument
kind: ClassDef
source_path: sldb/selfdoc/planned_document.py
source_span: '21:47'
source_sha256: 219eb47bdf2a28ef0f9d3f03e881bed785bec0b8a55903fbd8cdc00066a907cc
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.selfdoc.planned_document:PlannedDocument; contract-sha256:15e6d31b54264888b0ddc53060ab8859984cf1d640f27c5d134a682e0aecac77
---

# PlannedDocument

## Signature

Not applicable.

## Docstring

---
id: sldb.selfdoc.planned_document.PlannedDocument
kind: core
tags: [type:code.symbol]

---
Carry one validated documentation change and its before-image to execution.

Materializers fill ``payload`` and ``markdown`` after a render/extract
roundtrip check; ``write_documents`` persists them through SLDB tracking
and ``inspect_documents`` reads them without writing. It is a planning
record, not a filesystem transaction: ``previous`` is the before-image
captured at planning time and ``changed`` flags parser-owned drift, while
the write path re-verifies the file before saving.

## Imports

["__future__", "pathlib", "pydantic", "sldb.models.knowledge_surface"]

## Purpose

Carry one validated documentation change and its before-image to execution.

## Architecture

Not documented.
