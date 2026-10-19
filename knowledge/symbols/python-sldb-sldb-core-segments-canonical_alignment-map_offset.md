---
id: python-sldb-sldb-core-segments-canonical_alignment-map_offset
system: sldb
module: sldb.core.segments.canonical_alignment
qualname: map_offset
kind: FunctionDef
source_path: sldb/core/segments/canonical_alignment.py
source_span: '34:49'
source_sha256: 63209856d57ebc37f565891e59046288cb7d72b59cb1688d6b47f1ec5e21941f
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.segments.canonical_alignment:map_offset; contract-sha256:934d017553e07943bfb8df07e4a2caa402d390bcc6776269742aa03b4a28af92
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

Carry one canonical offset over to the raw text.

## Architecture

Not documented.
