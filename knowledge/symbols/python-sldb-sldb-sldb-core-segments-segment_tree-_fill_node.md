---
id: python-sldb-sldb-sldb-core-segments-segment_tree-_fill_node
system: sldb
module: sldb.sldb.core.segments.segment_tree
qualname: _fill_node
kind: FunctionDef
source_path: sldb/core/segments/segment_tree.py
source_span: 53:66
source_sha256: d0781963eb802dc9bfa2e75b86eccf4adefa98c50dce0879f7490fa791f420d4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.segment_tree:_fill_node; contract-sha256:a7b62000475ab7c77e056ddfadaa7e3439bc507eb48a4e27972d6bee8098d8d9
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

Not documented.

## Architecture

Not documented.
