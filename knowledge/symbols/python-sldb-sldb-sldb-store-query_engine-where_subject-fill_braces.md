---
id: python-sldb-sldb-sldb-store-query_engine-where_subject-fill_braces
system: sldb
module: sldb.sldb.store.query_engine.where_subject
qualname: fill_braces
kind: FunctionDef
source_path: sldb/store/query_engine/where_subject.py
source_span: '21:35'
source_sha256: 61951821d053f402c65bcac21e3b7664fb6f80493ec90e49ad77fa1fe5171889
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.query_engine.where_subject:fill_braces;
  contract-sha256:72d4576cf37aad592efe64fa649d07b73062f61df27d47d4422c7152ae607213
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

Not documented.

## Architecture

Not documented.
