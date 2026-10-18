---
id: python-sldb-sldb-cli-serve-unavailable_models-unavailable_models
system: sldb
module: sldb.cli.serve.unavailable_models
qualname: unavailable_models
kind: FunctionDef
source_path: sldb/cli/serve/unavailable_models.py
source_span: '23:33'
source_sha256: 6a4b28b96d1af8e5475e78d35b6da6d1040ba7b84a44136c6bff7a38cfe087a9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.unavailable_models:unavailable_models;
  contract-sha256:39265c76e2cbd089d2dc3806100763e3a88ee2e2b4e9e6aceca7e318c3118a13
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
