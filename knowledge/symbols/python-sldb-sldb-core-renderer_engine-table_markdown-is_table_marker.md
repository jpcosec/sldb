---
id: python-sldb-sldb-core-renderer_engine-table_markdown-is_table_marker
system: sldb
module: sldb.core.renderer_engine.table_markdown
qualname: is_table_marker
kind: FunctionDef
source_path: sldb/core/renderer_engine/table_markdown.py
source_span: '13:22'
source_sha256: 4c3f64b1402b72bd52c02bf510048156623258c950b602d8198c5afc74d887ac
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.table_markdown:is_table_marker;
  contract-sha256:15c970a7f16618f2647f767694bab26d4ecd8034004d578652fca06593f7d9c5
---

# is_table_marker

## Signature

is_table_marker(marker: Any)

## Docstring

Whether a marker asks for a Markdown table.

Args:
    marker: A parsed marker.

Returns:
    True when any trait is ``table`` or ``table[...]``.

## Imports

["__future__", "typing"]

## Purpose

Whether a marker asks for a Markdown table.

## Architecture

Not documented.
