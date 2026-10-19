---
id: python-sldb-sldb-store-query_engine-where_parse-compile_where
system: sldb
module: sldb.store.query_engine.where_parse
qualname: compile_where
kind: FunctionDef
source_path: sldb/store/query_engine/where_parse.py
source_span: '29:35'
source_sha256: 235d208fdacda7e8124041a424e53867d62bc761819c113663cd8b21bc983f00
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.query_engine.where_parse:compile_where; contract-sha256:f72056297ec5cfcf9dee7012a2cec64068bd03c990886844f61d51ccded01763
---

# compile_where

## Signature

compile_where(expression: str)

## Docstring

Parses one --where predicate, or several joined by ` and ` (all must hold); raises
WherePredicateError naming the first part no evaluator parses.

## Imports

["__future__", "re", "sldb.store.exceptions", "sldb.store.query_engine.where_literal", "typing"]

## Purpose

Parses one --where predicate, or several joined by ` and ` (all must hold); raises WherePredicateError naming the first part no evaluator parses.

## Architecture

Not documented.
