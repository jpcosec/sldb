---
id: python-sldb-sldb-core-segments-span_nesting-nest_nodes
system: sldb
module: sldb.core.segments.span_nesting
qualname: nest_nodes
kind: FunctionDef
source_path: sldb/core/segments/span_nesting.py
source_span: '16:33'
source_sha256: cd2f1c89f4f7cbff94cdfa309c4d993fe721b9e511081a682218bc78fbf530d5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.span_nesting:nest_nodes; contract-sha256:f1bd582dbc982b5d235381d9d75efa9b7419415160bfded40c5366fb81ec987d
---

# nest_nodes

## Signature

nest_nodes(nodes: list[dict[str, Any]])

## Docstring

Nest overlapping segments by containment.

Args:
    nodes: Flat segment dicts carrying ``start``, ``end`` and ``_order``.

Returns:
    The root segments, with contained segments moved into ``children``.

## Imports

["__future__", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
