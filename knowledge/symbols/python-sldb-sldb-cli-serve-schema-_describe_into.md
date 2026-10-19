---
id: python-sldb-sldb-cli-serve-schema-_describe_into
system: sldb
module: sldb.cli.serve.schema
qualname: _describe_into
kind: FunctionDef
source_path: sldb/cli/serve/schema.py
source_span: '45:50'
source_sha256: 76f8b45e5120c346a3c61e1323aee0a30ab7eea163c4cb893e47708b9fcb0f31
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.schema:_describe_into; contract-sha256:de0bc354953374b37993e3a87f54f0080cc8be73fac22c665eef2f2e492ce876
---

# _describe_into

## Signature

_describe_into(entry: Any, pythonpath: str, described: list[dict[str, Any]], unavailable: list[UnavailableModel])

## Docstring

Describe one model into ``described``, or record why it could not be.

## Imports

["__future__", "enum", "pathlib", "pydantic_core", "sldb.api.schema.field_descriptor", "sldb.api.schema.field_kinds", "sldb.api.schema.store_schema", "sldb.api.schema.unavailable_model", "sldb.cli.model_utils", "sldb.models.structured_doc", "sldb.store.io", "typing"]

## Purpose

Describe one model into ``described``, or record why it could not be.

## Architecture

Not documented.
