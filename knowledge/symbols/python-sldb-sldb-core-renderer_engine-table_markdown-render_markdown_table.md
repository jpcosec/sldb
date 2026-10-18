---
id: python-sldb-sldb-core-renderer_engine-table_markdown-render_markdown_table
system: sldb
module: sldb.core.renderer_engine.table_markdown
qualname: render_markdown_table
kind: FunctionDef
source_path: sldb/core/renderer_engine/table_markdown.py
source_span: '44:59'
source_sha256: 4c3f64b1402b72bd52c02bf510048156623258c950b602d8198c5afc74d887ac
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.table_markdown:render_markdown_table;
  contract-sha256:bd6dc0805550bcd19f42b55ef1a98761ae62ff37800b1dddb62e64e940dbaf57
---

# render_markdown_table

## Signature

render_markdown_table(value: Any, columns: list[str])

## Docstring

A Markdown table for ``value`` over ``columns``.

Args:
    value: The rows to render; anything not a list renders as headers only.
    columns: The column names, in order.

Returns:
    The table as Markdown, or a one-empty-column table when no columns.

## Imports

["__future__", "typing"]

## Purpose

A Markdown table for ``value`` over ``columns``.

## Architecture

Not documented.
