---
id: python-sldb-sldb-sldb-api-documents-heading_scan-scan_headings
system: sldb
module: sldb.sldb.api.documents.heading_scan
qualname: scan_headings
kind: FunctionDef
source_path: sldb/api/documents/heading_scan.py
source_span: '17:28'
source_sha256: 18d1b99a07f3afc58ac07180ccaf7c2d743bcb31d6155c04c18b398b87b4d728
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.heading_scan:scan_headings;
  contract-sha256:e6342659c1eb1a071f7be46b5a03b2fe7aacd20ec2b6904d043695129b6a320b
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
