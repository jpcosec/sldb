---
id: python-sldb-sldb-api-documents-heading_scan-scan_headings
system: sldb
module: sldb.api.documents.heading_scan
qualname: scan_headings
kind: FunctionDef
source_path: sldb/api/documents/heading_scan.py
source_span: '17:28'
source_sha256: 18d1b99a07f3afc58ac07180ccaf7c2d743bcb31d6155c04c18b398b87b4d728
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.heading_scan:scan_headings; contract-sha256:05acad1c66ade9bc70d9f332dbd83c4abd75e3b9c25c4f5591cecd92a3edb60c
---

# scan_headings

## Signature

scan_headings(markdown: str)

## Docstring

Every heading in `markdown`, in document order.

Args:
    markdown: The Markdown source (a template or a rendered document).

Returns:
    One `(level, title)` pair per heading; `level` is 1 for `#`, 2 for `##`.

## Imports

["__future__", "re", "sldb.core.ast", "sldb.core.contracts"]

## Purpose

Not documented.

## Architecture

Not documented.
