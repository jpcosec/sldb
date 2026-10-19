---
id: python-sldb-sldb-core-renderer_engine-table_markdown-table_columns
system: sldb
module: sldb.core.renderer_engine.table_markdown
qualname: table_columns
kind: FunctionDef
source_path: sldb/core/renderer_engine/table_markdown.py
source_span: '25:41'
source_sha256: 4c3f64b1402b72bd52c02bf510048156623258c950b602d8198c5afc74d887ac
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.table_markdown:table_columns;
  contract-sha256:670de7782534cb6f7f413b6f161ff8b02d154692901e823e12de30446a10143c
---

# table_columns

## Signature

table_columns(marker: Any, value: Any)

## Docstring

Column names for a table marker, declared or inferred from the first row.

Args:
    marker: A parsed marker carrying the table trait.
    value: The value to render, normally a list of rows.

Returns:
    The column names, empty when none can be determined.

## Imports

["__future__", "typing"]

## Purpose

Column names for a table marker, declared or inferred from the first row.

## Architecture

Not documented.
