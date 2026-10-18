---
id: python-sldb-sldb-cli-serve-save_routes-apply_change
system: sldb
module: sldb.cli.serve.save_routes
qualname: apply_change
kind: FunctionDef
source_path: sldb/cli/serve/save_routes.py
source_span: 94:107
source_sha256: 408aea16fbc3ba42fb7534082f884f5d7ded4f54a81587ca07b1bf42b5d8ff38
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.save_routes:apply_change; contract-sha256:a8b5d7d2afdf1b7f299904bdb4af02e80cbd1be50b9379eef742f7a46d5be32b
---

# apply_change

## Signature

apply_change(change: dict[str, Any], current: Any, path: Path | None, store_path: Path, pythonpath: str)

## Docstring

Apply one prevalidated change; `delete` is the inverse of `create`, file included.

`create` writes the Markdown file, so `delete` removes it. Untracking instead would
drop the document from the graph and leave the file on disk, where the next track or
rescan of the directory resurrects it.

## Imports

["__future__", "pathlib", "sldb.api.documents.create_document", "sldb.api.documents.delete_document", "sldb.api.documents.payload_save", "sldb.cli.model_utils", "sldb.cli.serve.save_plan", "sldb.cli.serve.save_single", "sldb.store.query", "threading", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
