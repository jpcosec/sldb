---
id: python-sldb-sldb-sldb-cli-serve-unavailable_models-_check
system: sldb
module: sldb.sldb.cli.serve.unavailable_models
qualname: _check
kind: FunctionDef
source_path: sldb/cli/serve/unavailable_models.py
source_span: '36:50'
source_sha256: 6a4b28b96d1af8e5475e78d35b6da6d1040ba7b84a44136c6bff7a38cfe087a9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.unavailable_models:_check; contract-sha256:a9ad0cad2a1e1d32ce0c6baba1a2714c7f7f151afc89999e5ae8fb4e26bb5777
---

# _check

## Signature

_check(entry: object, pythonpath: str)

## Docstring

Try to import one registered model.

Args:
    entry: The store index entry of the model.
    pythonpath: Directory to import the model module from.

Returns:
    None when the model loads, else the failure with its reason.

## Imports

["__future__", "pathlib", "sldb.api.schema.unavailable_model", "sldb.cli.model_utils", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
