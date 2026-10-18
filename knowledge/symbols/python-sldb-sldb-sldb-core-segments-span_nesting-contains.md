---
id: python-sldb-sldb-sldb-core-segments-span_nesting-contains
system: sldb
module: sldb.sldb.core.segments.span_nesting
qualname: contains
kind: FunctionDef
source_path: sldb/core/segments/span_nesting.py
source_span: '36:46'
source_sha256: cd2f1c89f4f7cbff94cdfa309c4d993fe721b9e511081a682218bc78fbf530d5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.span_nesting:contains; contract-sha256:b2d45e26528d355d85c0626b2854a70efb1768c43b10ed7e9c0823dd07d7a921
---

# contains

## Signature

contains(outer: dict[str, Any], inner: dict[str, Any])

## Docstring

Whether ``outer`` spans over ``inner``.

Args:
    outer: The candidate containing segment.
    inner: The candidate contained segment.

Returns:
    True when inner's range fits inside outer's range.

## Imports

["__future__", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
