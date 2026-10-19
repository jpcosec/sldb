---
id: python-sldb-sldb-cli-serve-unavailable_models-_check
system: sldb
module: sldb.cli.serve.unavailable_models
qualname: _check
kind: FunctionDef
source_path: sldb/cli/serve/unavailable_models.py
source_span: '36:50'
source_sha256: 6a4b28b96d1af8e5475e78d35b6da6d1040ba7b84a44136c6bff7a38cfe087a9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.unavailable_models:_check; contract-sha256:8c7addafddf6908ef9ec7d29b2feb0727ba3fd8eb21cd2694eb8be959c568af1
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

Try to import one registered model.

## Architecture

Not documented.
