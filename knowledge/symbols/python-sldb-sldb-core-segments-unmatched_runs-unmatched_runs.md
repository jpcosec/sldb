---
id: python-sldb-sldb-core-segments-unmatched_runs-unmatched_runs
system: sldb
module: sldb.core.segments.unmatched_runs
qualname: unmatched_runs
kind: FunctionDef
source_path: sldb/core/segments/unmatched_runs.py
source_span: '18:29'
source_sha256: f687fe703f11558b26bfeef4f2b2fe94ecd210b31602023ccd1d769e8caea220
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.segments.unmatched_runs:unmatched_runs; contract-sha256:8d624f5611f3ec8b2831350a1a48f7b25c8fae99657b78491ef411f12ed7d9ec
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

Every run of ``raw`` the canonical render does not account for.

## Architecture

Not documented.
