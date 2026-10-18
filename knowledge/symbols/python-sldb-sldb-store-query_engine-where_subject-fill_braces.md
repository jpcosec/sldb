---
id: python-sldb-sldb-store-query_engine-where_subject-fill_braces
system: sldb
module: sldb.store.query_engine.where_subject
qualname: fill_braces
kind: FunctionDef
source_path: sldb/store/query_engine/where_subject.py
source_span: '21:35'
source_sha256: 61951821d053f402c65bcac21e3b7664fb6f80493ec90e49ad77fa1fe5171889
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.query_engine.where_subject:fill_braces; contract-sha256:8f70faac27b671656c2ecbb46605973049d33c6cf7ba35aec71be9c2e563d549
---

# fill_braces

## Signature

fill_braces(expression: str, subject: dict[str, Any])

## Docstring

`expression` with every `{field}` replaced by the subject's value, and whether all were.

A brace that cannot be filled becomes a placeholder literal, so the expression still parses.

## Imports

["__future__", "re", "sldb.store.query_engine.where_literal", "sldb.store.query_engine.where_parse", "types", "typing"]

## Purpose

`expression` with every `{field}` replaced by the subject's value, and whether all were.

## Architecture

Not documented.
