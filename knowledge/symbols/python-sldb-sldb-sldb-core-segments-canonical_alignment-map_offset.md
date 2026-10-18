---
id: python-sldb-sldb-sldb-core-segments-canonical_alignment-map_offset
system: sldb
module: sldb.sldb.core.segments.canonical_alignment
qualname: map_offset
kind: FunctionDef
source_path: sldb/core/segments/canonical_alignment.py
source_span: '34:49'
source_sha256: 63209856d57ebc37f565891e59046288cb7d72b59cb1688d6b47f1ec5e21941f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.canonical_alignment:map_offset;
  contract-sha256:479737d64c88afaa1d5a3c400b62f75e590faf3b05839fecd86d5ee1cf216e3c
---

# map_offset

## Signature

map_offset(opcodes: list[Opcode], position: int, is_end: bool=False)

## Docstring

Carry one canonical offset over to the raw text.

Args:
    opcodes: The alignment from :func:`align`.
    position: The canonical offset to map.
    is_end: Whether the offset is an exclusive end, which makes it belong to
        the run ending at it rather than the one starting there.

Returns:
    The raw offset and whether it landed inside an ``equal`` run.

## Imports

["__future__", "difflib"]

## Purpose

Not documented.

## Architecture

Not documented.
