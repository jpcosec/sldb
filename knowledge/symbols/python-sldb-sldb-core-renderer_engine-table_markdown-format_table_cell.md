---
id: python-sldb-sldb-core-renderer_engine-table_markdown-format_table_cell
system: sldb
module: sldb.core.renderer_engine.table_markdown
qualname: format_table_cell
kind: FunctionDef
source_path: sldb/core/renderer_engine/table_markdown.py
source_span: 62:73
source_sha256: 4c3f64b1402b72bd52c02bf510048156623258c950b602d8198c5afc74d887ac
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.table_markdown:format_table_cell;
  contract-sha256:3c2b0bda1c27d6a6a469cd3ee51f33415f63fed75361877aec02771b50722d98
---

# format_table_cell

## Signature

format_table_cell(value: Any)

## Docstring

One cell's text, with newlines flattened and pipes escaped.

Args:
    value: The cell value; None renders empty.

Returns:
    The cell's Markdown-safe text.

## Imports

["__future__", "typing"]

## Purpose

One cell's text, with newlines flattened and pipes escaped.

## Architecture

Not documented.
