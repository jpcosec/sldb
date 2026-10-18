---
id: python-sldb-sldb-core-segments-segment_tree-build_segment_tree
system: sldb
module: sldb.core.segments.segment_tree
qualname: build_segment_tree
kind: FunctionDef
source_path: sldb/core/segments/segment_tree.py
source_span: '16:26'
source_sha256: d0781963eb802dc9bfa2e75b86eccf4adefa98c50dce0879f7490fa791f420d4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.segment_tree:build_segment_tree;
  contract-sha256:6d261b7918dddef486cd11bd08fe9372c2def028dba1504ab29ea2dd96b490a6
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

The full segment sequence for ``text``: nested nodes with literals between them.

## Architecture

Not documented.
