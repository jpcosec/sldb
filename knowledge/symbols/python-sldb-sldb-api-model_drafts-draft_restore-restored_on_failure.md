---
id: python-sldb-sldb-api-model_drafts-draft_restore-restored_on_failure
system: sldb
module: sldb.api.model_drafts.draft_restore
qualname: restored_on_failure
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_restore.py
source_span: '23:30'
source_sha256: 8960650d839e20d46186bf99cf291015c44a94e377ae84ce59d9087919e9ccb9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_restore:restored_on_failure;
  contract-sha256:5cbd4411d16b9412cc357bf771a17953388a26bac0ad56962992db4797f4f7a3
---

# restored_on_failure

## Signature

restored_on_failure(paths: list[Path])

## Docstring

Snapshot ``paths``; if the block raises, write them back and re-raise.

## Imports

["__future__", "collections.abc", "contextlib", "pathlib", "sldb.api.stores.open_store", "sldb.store.layout"]

## Purpose

Snapshot ``paths``; if the block raises, write them back and re-raise.

## Architecture

Not documented.
