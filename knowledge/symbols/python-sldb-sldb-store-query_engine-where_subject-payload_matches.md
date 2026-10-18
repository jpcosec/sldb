---
id: python-sldb-sldb-store-query_engine-where_subject-payload_matches
system: sldb
module: sldb.store.query_engine.where_subject
qualname: payload_matches
kind: FunctionDef
source_path: sldb/store/query_engine/where_subject.py
source_span: '38:48'
source_sha256: 61951821d053f402c65bcac21e3b7664fb6f80493ec90e49ad77fa1fe5171889
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.query_engine.where_subject:payload_matches;
  contract-sha256:4fca2e32166bf09e9d19f045198e21a5d4fff94bcf807a0c7c673a97276966bf
---

# payload_matches

## Signature

payload_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None=None, name: str='')

## Docstring

Whether `expression` holds on `payload`; `{field}` reads `subject` (default: `payload`).

`doc ~ "..."` reads `name`; `model <= X` never holds, a payload carries no model class.
An empty expression always holds. Raises WherePredicateError when it does not parse.

## Imports

["__future__", "re", "sldb.store.query_engine.where_literal", "sldb.store.query_engine.where_parse", "types", "typing"]

## Purpose

Whether `expression` holds on `payload`; `{field}` reads `subject` (default: `payload`).

## Architecture

Not documented.
