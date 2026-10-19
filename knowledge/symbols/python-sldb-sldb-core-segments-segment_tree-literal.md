---
id: python-sldb-sldb-core-segments-segment_tree-literal
system: sldb
module: sldb.core.segments.segment_tree
qualname: literal
kind: FunctionDef
source_path: sldb/core/segments/segment_tree.py
source_span: 69:80
source_sha256: d0781963eb802dc9bfa2e75b86eccf4adefa98c50dce0879f7490fa791f420d4
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.segments.segment_tree:literal; contract-sha256:bdd1289db4a7b32ff3427ef73f0b62a29f1150390a01fafd5c7439cd6035271c
---

# literal

## Signature

literal(text: str, start: int, end: int)

## Docstring

A literal segment over ``text[start:end]``.

Args:
    text: The canonical text.
    start: Inclusive start offset.
    end: Exclusive end offset.

Returns:
    A ``literal`` segment dict.

## Imports

["__future__", "sldb.core.segments.span_nesting", "typing"]

## Purpose

A literal segment over ``text[start:end]``.

## Architecture

Not documented.
