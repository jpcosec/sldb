---
id: python-sldb-sldb-selfdoc-python_source_values-relative_module
system: sldb
module: sldb.selfdoc.python_source_values
qualname: relative_module
kind: FunctionDef
source_path: sldb/selfdoc/python_source_values.py
source_span: '46:54'
source_sha256: 756b4c05996cac9991c316dfb353e52a8a72764a65ebee535404fb0c0dda92e1
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.selfdoc.python_source_values:relative_module; contract-sha256:d5916a567678c99f12e3f4a996d9dfd9d5dbbc2e9b3bdfa8e518e33ff132ec17
---

# relative_module

## Signature

relative_module(module: str, requested: str | None, level: int, is_package: bool=False)

## Docstring

Resolve an ImportFrom module spelling against its importer's package: a package's
`__init__` is its own package (`from .impl import X` in `pkg/inner/__init__.py` names
`pkg.inner.impl`, which was resolved as `pkg.impl`).

## Imports

["__future__", "ast", "hashlib"]

## Purpose

Not documented.

## Architecture

Not documented.
