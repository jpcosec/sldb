---
id: python-sldb-sldb-core-segments-unmatched_runs-trimmed
system: sldb
module: sldb.core.segments.unmatched_runs
qualname: trimmed
kind: FunctionDef
source_path: sldb/core/segments/unmatched_runs.py
source_span: '32:46'
source_sha256: f687fe703f11558b26bfeef4f2b2fe94ecd210b31602023ccd1d769e8caea220
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.segments.unmatched_runs:trimmed; contract-sha256:58bc2972fe1d3e7a4fb495849c5a47c6dc1087d53485c8d977c56bed2cf29083
---

# trimmed

## Signature

trimmed(text: str, start: int, end: int)

## Docstring

A range with its surrounding whitespace excluded from the offsets.

Args:
    text: The text the offsets address.
    start: Inclusive start offset.
    end: Exclusive end offset.

Returns:
    A ``{start, end, text}`` range tightened to the non-blank content.

## Imports

["__future__", "sldb.core.segments.canonical_alignment", "typing"]

## Purpose

A range with its surrounding whitespace excluded from the offsets.

## Architecture

Not documented.
