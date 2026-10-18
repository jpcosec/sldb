---
id: python-sldb-sldb-models-structured_doc-structurednldoc-compose_field
system: sldb
module: sldb.models.structured_doc
qualname: StructuredNLDoc.compose_field
kind: FunctionDef
source_path: sldb/models/structured_doc.py
source_span: '35:50'
source_sha256: 4ee4e777b82fa5ae9f897579af1be36bdd502f7088896788dcaae05597bcc4cf
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.models.structured_doc:StructuredNLDoc.compose_field;
  contract-sha256:60d731d6b6a48686c76a440324aa44d536438db74bbf2e5802635495c0d16c92
---

# StructuredNLDoc.compose_field

## Signature

compose_field(self, name: str, recorder: Any=None, ref_root: Path | None=None)

## Docstring

The composed field's text. `ref_root` resolves relative refs; the CWD is the fallback.

A composition ref is a path in the project (`docs/tasks/task-a.md`), not a path
relative to wherever the process happens to be running. Resolving it against the CWD
made the same document compose differently depending on the caller's directory —
silently, because a ref that does not resolve renders as empty text.

## Imports

["__future__", "importlib", "pathlib", "pydantic", "typing"]

## Purpose

The composed field's text. `ref_root` resolves relative refs; the CWD is the fallback.

## Architecture

Not documented.
