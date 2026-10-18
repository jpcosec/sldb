---
id: python-sldb-sldb-sldb-core-segments-canonical_alignment-_covers
system: sldb
module: sldb.sldb.core.segments.canonical_alignment
qualname: _covers
kind: FunctionDef
source_path: sldb/core/segments/canonical_alignment.py
source_span: 52:64
source_sha256: 63209856d57ebc37f565891e59046288cb7d72b59cb1688d6b47f1ec5e21941f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.canonical_alignment:_covers;
  contract-sha256:a3adc5143613357244ef0b13efbd60591a643f2e8313754e8bb86bf4ac40effe
---

# _covers

## Signature

_covers(i1: int, i2: int, position: int, is_end: bool)

## Docstring

Whether an opcode's canonical range contains ``position``.

Args:
    i1: Inclusive start of the opcode's canonical range.
    i2: Exclusive end of the opcode's canonical range.
    position: The canonical offset being placed.
    is_end: Whether the offset is an exclusive end.

Returns:
    True when the offset belongs to this run.

## Imports

["__future__", "difflib"]

## Purpose

Not documented.

## Architecture

Not documented.
