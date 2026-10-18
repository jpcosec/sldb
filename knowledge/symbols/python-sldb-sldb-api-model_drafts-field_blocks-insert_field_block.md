---
id: python-sldb-sldb-api-model_drafts-field_blocks-insert_field_block
system: sldb
module: sldb.api.model_drafts.field_blocks
qualname: insert_field_block
kind: FunctionDef
source_path: sldb/api/model_drafts/field_blocks.py
source_span: '20:38'
source_sha256: 67b3ee754b0bb3851ecc2a062f0d025fca71e1d45d8b2d83ec47b9fe2995c0cd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.field_blocks:insert_field_block;
  contract-sha256:699a3ec6bae61e30d7057e490cfb0dfbd5db2e934c1d1d5270af92eac0931c25
---

# insert_field_block

## Signature

insert_field_block(path: Path, cls_name: str, f_name: str, f_block: str)

## Docstring

The source of `path` with `f_block` appended to the body of class `cls_name`.

The source is normalized to end in exactly one newline first
(`_ensure_final_newline`) so the inserted block never ends up concatenated
to the previous line. sldb writes model sources procedurally and owns the
canonical output form (LF + a single final newline); line endings of files
that were edited by hand are normalized rather than preserved.

Raises:
    SLDBModelEditError: When the class is missing or already declares the field.

## Imports

["__future__", "ast", "pathlib", "sldb.api.model_drafts.source_editing", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
