---
id: python-sldb-sldb-sldb-core-segments-segment_tree-build_segment_tree
system: sldb
module: sldb.sldb.core.segments.segment_tree
qualname: build_segment_tree
kind: FunctionDef
source_path: sldb/core/segments/segment_tree.py
source_span: '16:26'
source_sha256: d0781963eb802dc9bfa2e75b86eccf4adefa98c50dce0879f7490fa791f420d4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.segment_tree:build_segment_tree;
  contract-sha256:e19152a167d8ac49c84bbb5209735aefb925ef1ed24fba33f9a786deb1c070aa
---

# build_segment_tree

## Signature

build_segment_tree(nodes: list[dict[str, Any]], text: str)

## Docstring

The full segment sequence for ``text``: nested nodes with literals between them.

Args:
    nodes: Flat segment dicts carrying ``start``, ``end`` and ``_order``.
    text: The canonical text the offsets address.

Returns:
    Top-level segments in reading order, each with a filled ``children`` list.

## Imports

["__future__", "sldb.core.segments.span_nesting", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
