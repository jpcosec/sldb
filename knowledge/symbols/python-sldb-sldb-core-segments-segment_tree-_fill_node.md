---
id: python-sldb-sldb-core-segments-segment_tree-_fill_node
system: sldb
module: sldb.core.segments.segment_tree
qualname: _fill_node
kind: FunctionDef
source_path: sldb/core/segments/segment_tree.py
source_span: 53:66
source_sha256: d0781963eb802dc9bfa2e75b86eccf4adefa98c50dce0879f7490fa791f420d4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.segment_tree:_fill_node; contract-sha256:302d5e88a5f5b40beb921ddab43d2a093f844d39a263ebec149d6e3fa63844e0
---

# _fill_node

## Signature

_fill_node(node: dict[str, Any], text: str)

## Docstring

Drop the ordering key of ``node`` and fill its children with literals.

Args:
    node: A nested segment dict carrying ``start``, ``end`` and ``children``.
    text: The canonical text the offsets address.

Returns:
    The same node, mutated, with a complete ``children`` sequence.

## Imports

["__future__", "sldb.core.segments.span_nesting", "typing"]

## Purpose

Drop the ordering key of ``node`` and fill its children with literals.

## Architecture

Not documented.
