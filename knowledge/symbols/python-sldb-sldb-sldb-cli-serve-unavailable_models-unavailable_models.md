---
id: python-sldb-sldb-sldb-cli-serve-unavailable_models-unavailable_models
system: sldb
module: sldb.sldb.cli.serve.unavailable_models
qualname: unavailable_models
kind: FunctionDef
source_path: sldb/cli/serve/unavailable_models.py
source_span: '23:33'
source_sha256: 6a4b28b96d1af8e5475e78d35b6da6d1040ba7b84a44136c6bff7a38cfe087a9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.unavailable_models:unavailable_models;
  contract-sha256:e855ea3e65e773e5672bfcea561cdc5fd16ba2c0cd4f8c9bffe992867d993440
---

# unavailable_models

## Signature

unavailable_models(store_path: Path, pythonpath: str)

## Docstring

Every registered model whose class cannot be imported right now.

Args:
    store_path: Path of the ``.sldb`` store.
    pythonpath: Directory to import the model modules from.

Returns:
    One entry per unloadable model, each with the reason it failed.

## Imports

["__future__", "pathlib", "sldb.api.schema.unavailable_model", "sldb.cli.model_utils", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
