---
id: python-sldb-sldb-core-segments-segment_tree-interleave_literals
system: sldb
module: sldb.core.segments.segment_tree
qualname: interleave_literals
kind: FunctionDef
source_path: sldb/core/segments/segment_tree.py
source_span: '29:50'
source_sha256: d0781963eb802dc9bfa2e75b86eccf4adefa98c50dce0879f7490fa791f420d4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.segment_tree:interleave_literals;
  contract-sha256:809ab095fe6264f4e27e88a88794675ca3a0bcd774df4cc6d5f6ae333c65d3e1
---

# interleave_literals

## Signature

interleave_literals(nodes: list[dict[str, Any]], text: str, lo: int, hi: int)

## Docstring

Insert literal segments for the text not covered by ``nodes``.

Args:
    nodes: Sibling segments, in reading order, inside ``[lo, hi)``.
    text: The canonical text the offsets address.
    lo: Start of the range being filled.
    hi: End of the range being filled.

Returns:
    The siblings with literal segments inserted before, between and after them.

## Imports

["__future__", "sldb.core.segments.span_nesting", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
