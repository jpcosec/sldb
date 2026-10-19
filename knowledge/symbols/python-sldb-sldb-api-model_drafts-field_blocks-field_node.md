---
id: python-sldb-sldb-api-model_drafts-field_blocks-field_node
system: sldb
module: sldb.api.model_drafts.field_blocks
qualname: field_node
kind: FunctionDef
source_path: sldb/api/model_drafts/field_blocks.py
source_span: 55:64
source_sha256: 67b3ee754b0bb3851ecc2a062f0d025fca71e1d45d8b2d83ec47b9fe2995c0cd
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.field_blocks:field_node; contract-sha256:a918ddcbbfba67e6e074ef12156ce3b11f65b2964fd3923d173f2d92d194df9c
---

# field_node

## Signature

field_node(class_node: ast.ClassDef, class_name: str, field_name: str)

## Docstring

The annotated assignment declaring a field.

Raises:
    SLDBModelEditError: When the class does not declare the field.

## Imports

["__future__", "ast", "pathlib", "sldb.api.model_drafts.source_editing", "sldb.core.exceptions", "typing"]

## Purpose

The annotated assignment declaring a field.

## Architecture

Not documented.
