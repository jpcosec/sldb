---
id: python-sldb-sldb-selfdoc-python_scanner-_one_per_name
system: sldb
module: sldb.selfdoc.python_scanner
qualname: _one_per_name
kind: FunctionDef
source_path: sldb/selfdoc/python_scanner.py
source_span: 58:68
source_sha256: 8581e7bc60802b1d8b38ce1767d0339b76147a7c9a88609cfaf526eed7010301
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.selfdoc.python_scanner:_one_per_name; contract-sha256:31ca82323ae27b460b67618d43cebf79e91a66cc8f49646bca2da65aafb56fdf
---

# _one_per_name

## Signature

_one_per_name(records: list[PythonSymbol])

## Docstring

One symbol per name bound in a scope: a property's setter (`@x.setter`) or an
`@overload` redefines the name, and two records for one name collided as one document id
(`selfdoc python-check` failed on `DocumentEntry.hash_c`). The first definition, which
carries the docstring, stands for the name and spans to the last.

## Imports

[".python_symbol", "__future__", "ast", "hashlib", "pathlib"]

## Purpose

One symbol per name bound in a scope: a property's setter (`@x.setter`) or an `@overload` redefines the name, and two records for one name collided as one document id (`selfdoc python-check` failed on `DocumentEntry.hash_c`). The first definition, which carries the docstring, stands for the name and spans to the last.

## Architecture

Not documented.
