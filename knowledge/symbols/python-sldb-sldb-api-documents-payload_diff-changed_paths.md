---
id: python-sldb-sldb-api-documents-payload_diff-changed_paths
system: sldb
module: sldb.api.documents.payload_diff
qualname: changed_paths
kind: FunctionDef
source_path: sldb/api/documents/payload_diff.py
source_span: '14:29'
source_sha256: a43590ef7e0c244eab9e7108917e9016541cfeed1d380b20c09a305e1306f396
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.payload_diff:changed_paths; contract-sha256:2c7a8b4f2935ad26c3f24c9371f8817f6ff63c8635426e992ebd2d491d2047e2
---

# changed_paths

## Signature

changed_paths(before: Any, after: Any)

## Docstring

Dotted paths whose values differ between `before` and `after`.

Dicts are compared recursively; a key removed or added appears as its own path,
and a nested change appears as `parent.child`. Non-dict values compared unequal
yield the empty string, which the caller turns into the root key.

## Imports

["__future__", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
