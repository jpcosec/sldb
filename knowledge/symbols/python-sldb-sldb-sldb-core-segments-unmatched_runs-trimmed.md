---
id: python-sldb-sldb-sldb-core-segments-unmatched_runs-trimmed
system: sldb
module: sldb.sldb.core.segments.unmatched_runs
qualname: trimmed
kind: FunctionDef
source_path: sldb/core/segments/unmatched_runs.py
source_span: '32:46'
source_sha256: f687fe703f11558b26bfeef4f2b2fe94ecd210b31602023ccd1d769e8caea220
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.unmatched_runs:trimmed; contract-sha256:4aca358d704feaaac98c59eaf66f55576486a2a9f36c60850b7b0a40192356e0
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

Not documented.

## Architecture

Not documented.
