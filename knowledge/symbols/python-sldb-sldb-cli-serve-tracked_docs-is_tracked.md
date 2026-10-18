---
id: python-sldb-sldb-cli-serve-tracked_docs-is_tracked
system: sldb
module: sldb.cli.serve.tracked_docs
qualname: is_tracked
kind: FunctionDef
source_path: sldb/cli/serve/tracked_docs.py
source_span: '15:32'
source_sha256: 7ae9eec0be578c90f9d6cc2115deebc00ca84d16b2d16b3e760528c5549108a4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.tracked_docs:is_tracked; contract-sha256:134637a3f149370dd453c7ebf3cb0bcd9bcf780bfd0e500992c0a6dfbeead6ff
---

# is_tracked

## Signature

is_tracked(store_path: Path, root: Path, name: str)

## Docstring

Whether any model in the store tracks a document called ``name``.

Args:
    store_path: Path of the ``.sldb`` store.
    root: Root the store's index paths are relative to.
    name: The document name to look for.

Returns:
    True when some model's document index lists that name.

## Imports

["__future__", "pathlib", "sldb.store.io"]

## Purpose

Whether any model in the store tracks a document called ``name``.

## Architecture

Not documented.
