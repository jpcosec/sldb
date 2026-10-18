---
id: python-sldb-sldb-core-renderer_engine-base-baserenderer-_is_absent_optional_line
system: sldb
module: sldb.core.renderer_engine.base
qualname: BaseRenderer._is_absent_optional_line
kind: FunctionDef
source_path: sldb/core/renderer_engine/base.py
source_span: 36:61
source_sha256: ba5267bf5d0dd0936ea61e5fb71183b5604f43d857c57f8dbfa7fa7fe6f763b5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.base:BaseRenderer._is_absent_optional_line;
  contract-sha256:3fba66b9283080c46494d354ed9ea881387e6d2676a983782fa341032acbb197
---

# BaseRenderer._is_absent_optional_line

## Signature

_is_absent_optional_line(self, line: str, data: dict[str, Any])

## Docstring

An optrev marker whose value is None leaves NO trace in the render:
its whole line is dropped, so the document reads byte-for-byte as if
the field were never declared (contract: 'It MAY BE ABSENT in the
document'). Only two shapes qualify: `key: ⸢optrev•key⸥` or
`⸢optrev•key⸥` alone on the line (leading whitespace allowed).

A line that SHARES its content with anything else -- a table row of
cells, a list bullet, preceding text, another marker -- is never
dropped; there the marker is replaced with the empty string (today's
behavior) because deleting the line would corrupt the surrounding
structure (a table would lose a column, a list item would vanish).
An empty list/dict VALUE (`[]`/`{}`) is not None, so it still renders
(as an empty table or empty mapping); only a None value means absent.

kind == 'render' markers are NOT optional-extractable fields: they
keep their historical empty-string behavior and are never the reason
a line is omitted.

## Imports

["__future__", "jinja2", "re", "sldb.core.handlers.utils", "sldb.core.renderer_engine.jinja_trailing", "sldb.core.renderer_engine.python_expr", "sldb.core.renderer_engine.table_markdown", "typing", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
