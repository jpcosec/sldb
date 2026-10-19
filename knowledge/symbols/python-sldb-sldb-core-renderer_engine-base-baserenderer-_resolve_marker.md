---
id: python-sldb-sldb-core-renderer_engine-base-baserenderer-_resolve_marker
system: sldb
module: sldb.core.renderer_engine.base
qualname: BaseRenderer._resolve_marker
kind: FunctionDef
source_path: sldb/core/renderer_engine/base.py
source_span: 70:86
source_sha256: ba5267bf5d0dd0936ea61e5fb71183b5604f43d857c57f8dbfa7fa7fe6f763b5
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.base:BaseRenderer._resolve_marker;
  contract-sha256:1fa30e6f71b7f13efe6c74ef56a827ffb9278a16c866d3440a44a2a0c49d5f75
---

# BaseRenderer._resolve_marker

## Signature

_resolve_marker(self, m: Any, match: re.Match, data: dict[str, Any])

## Docstring

The rendered surface of one marker, or the literal marker when unresolved.

Args:
    m: The parsed marker.
    match: The regex match of the marker in the template line.
    data: The payload the marker reads from.

Returns:
    The value's text, an empty string for an absent optional, or the
    literal marker when the value is missing and required.

## Imports

["__future__", "jinja2", "re", "sldb.core.handlers.utils", "sldb.core.renderer_engine.jinja_trailing", "sldb.core.renderer_engine.python_expr", "sldb.core.renderer_engine.table_markdown", "typing", "yaml"]

## Purpose

The rendered surface of one marker, or the literal marker when unresolved.

## Architecture

Not documented.
