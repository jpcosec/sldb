---
id: python-sldb-sldb-core-segments-canonical_alignment-align
system: sldb
module: sldb.core.segments.canonical_alignment
qualname: align
kind: FunctionDef
source_path: sldb/core/segments/canonical_alignment.py
source_span: '20:31'
source_sha256: 63209856d57ebc37f565891e59046288cb7d72b59cb1688d6b47f1ec5e21941f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.canonical_alignment:align; contract-sha256:14a41b5c99adc42addb2e296cd55ee5b59e320dea154320371362f7dd1fe714d
---

# align

## Signature

align(canonical: str, raw: str)

## Docstring

The character-level opcodes taking ``canonical`` to ``raw``.

Args:
    canonical: The re-rendered text the spans address.
    raw: The markdown the payload was extracted from.

Returns:
    ``SequenceMatcher`` opcodes, computed without autojunk so long texts
    are not silently treated as junk-heavy and mis-aligned.

## Imports

["__future__", "difflib"]

## Purpose

Not documented.

## Architecture

Not documented.
