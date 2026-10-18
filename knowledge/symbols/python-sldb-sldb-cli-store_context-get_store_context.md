---
id: python-sldb-sldb-cli-store_context-get_store_context
system: sldb
module: sldb.cli.store_context
qualname: get_store_context
kind: FunctionDef
source_path: sldb/cli/store_context.py
source_span: '19:24'
source_sha256: 1c6067c91e06a803b26f1667f2220f882c6f813e0df8fb9408c3d9308304a42e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.store_context:get_store_context; contract-sha256:f85814f0abffbe146c21aa669537967e49e555dcca460507376c6f542eb59133
---

# get_store_context

## Signature

get_store_context(store_arg: str | None, mode: str='default')

## Docstring

Resolves once per Store/World opened (pron: once per session) or per sldb CLI command
— the natural "start of an operation" a fresh document-leaf sweep belongs to (PLAN 15
capa 6: `new_operation` schedules that sweep for the next `runtime_cache.signature`).

## Imports

["__future__", "pathlib", "sldb.api.stores.open_store", "sldb.api.stores.store_discovery"]

## Purpose

Resolves once per Store/World opened (pron: once per session) or per sldb CLI command — the natural "start of an operation" a fresh document-leaf sweep belongs to (PLAN 15 capa 6: `new_operation` schedules that sweep for the next `runtime_cache.signature`).

## Architecture

Not documented.
