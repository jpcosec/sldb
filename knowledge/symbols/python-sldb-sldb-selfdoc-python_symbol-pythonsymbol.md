---
id: python-sldb-sldb-selfdoc-python_symbol-pythonsymbol
system: sldb
module: sldb.selfdoc.python_symbol
qualname: PythonSymbol
kind: ClassDef
source_path: sldb/selfdoc/python_symbol.py
source_span: '17:44'
source_sha256: 7ac5b65bb0541e476b6e63be7cb5cd663bfe8f2337d79b989dd316d5ad895786
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.selfdoc.python_symbol:PythonSymbol; contract-sha256:1a344fc4d8e462dabb868f097ea93211bad5dfe4740dc94c9559c5ae547bf448
---

# PythonSymbol

## Signature

Not applicable.

## Docstring

---
id: sldb.selfdoc.python_symbol.PythonSymbol
kind: core
tags: [type:code.symbol]

---
Validate and carry the static facts extracted from one Python declaration.

The scanner supplies lexical identity, AST kind, source location, signature,
docstring, enclosing-module imports, and a hash of the entire source file.
The materializer consumes these fields to build a tracked reference document.
The record does not resolve imports or establish runtime dependencies; its
file hash is not a symbol-level fingerprint. Field ``kind`` describes the AST
node, independently of the semantic ``kind`` in this docstring's metadata.

## Imports

["__future__", "pydantic"]

## Purpose

Not documented.

## Architecture

Not documented.
