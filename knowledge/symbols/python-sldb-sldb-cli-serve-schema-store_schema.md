---
id: python-sldb-sldb-cli-serve-schema-store_schema
system: sldb
module: sldb.cli.serve.schema
qualname: store_schema
kind: FunctionDef
source_path: sldb/cli/serve/schema.py
source_span: '31:42'
source_sha256: 76f8b45e5120c346a3c61e1323aee0a30ab7eea163c4cb893e47708b9fcb0f31
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.schema:store_schema; contract-sha256:b9fca33cb9ac43773c5fc252ab4f15ca30fc03dda885672e7111dc041a250e8b
---

# store_schema

## Signature

store_schema(store_path: Path, pythonpath: str)

## Docstring

Describe every registered model, declaring the ones that cannot load.

A model whose module does not import must not take the listing down: a store
with twenty models and one broken has nineteen describable models and one
reportable failure, not zero models.

## Imports

["__future__", "enum", "pathlib", "pydantic_core", "sldb.api.schema.field_descriptor", "sldb.api.schema.field_kinds", "sldb.api.schema.store_schema", "sldb.api.schema.unavailable_model", "sldb.cli.model_utils", "sldb.models.structured_doc", "sldb.store.io", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
