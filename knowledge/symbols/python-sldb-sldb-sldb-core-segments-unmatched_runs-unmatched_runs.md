---
id: python-sldb-sldb-sldb-core-segments-unmatched_runs-unmatched_runs
system: sldb
module: sldb.sldb.core.segments.unmatched_runs
qualname: unmatched_runs
kind: FunctionDef
source_path: sldb/core/segments/unmatched_runs.py
source_span: '18:29'
source_sha256: f687fe703f11558b26bfeef4f2b2fe94ecd210b31602023ccd1d769e8caea220
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.unmatched_runs:unmatched_runs;
  contract-sha256:ed30bbb0faed5d4d63d1dbb649b60275b94255a8e55218fe71b6b535139f5b2e
---

# unmatched_runs

## Signature

unmatched_runs(opcodes: list[Opcode], raw: str)

## Docstring

Every run of ``raw`` the canonical render does not account for.

Args:
    opcodes: The alignment from :func:`sldb.core.segments.canonical_alignment.align`.
    raw: The markdown the payload was extracted from.

Returns:
    Trimmed ``{start, end, text}`` ranges, blank ones removed.

## Imports

["__future__", "sldb.core.segments.canonical_alignment", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
