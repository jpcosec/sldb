---
id: python-sldb-sldb-api-model_drafts-draft_restore-_restore
system: sldb
module: sldb.api.model_drafts.draft_restore
qualname: _restore
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_restore.py
source_span: '33:39'
source_sha256: 8960650d839e20d46186bf99cf291015c44a94e377ae84ce59d9087919e9ccb9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_restore:_restore; contract-sha256:c41d003b9563c18d9b234d5347fa661ace807fee3fd7e4105fe913be5598cd8d
---

# _restore

## Signature

_restore(snapshot: dict[Path, bytes | None])

## Docstring

Write every snapshotted file back, deleting the ones that did not exist.

## Imports

["__future__", "collections.abc", "contextlib", "pathlib", "sldb.api.stores.open_store", "sldb.store.layout"]

## Purpose

Write every snapshotted file back, deleting the ones that did not exist.

## Architecture

Not documented.
