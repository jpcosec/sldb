---
id: python-sldb-sldb-api-where-where_matches
system: sldb
module: sldb.api.where
qualname: where_matches
kind: FunctionDef
source_path: sldb/api/where.py
source_span: '10:23'
source_sha256: cf928a640518f596de220a88541cbfce620f3a2e6e5b45c74f2692b920c61834
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.where:where_matches; contract-sha256:48151e2b2aacd35de2115cc10e89e13b9e9e388590773c4684635ac889edf390
---

# where_matches

## Signature

where_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None=None)

## Docstring

Whether a `--where` predicate holds on `payload` (the grammar of `sldb find --where`).

Args:
    expression: Predicates joined by ` and `: `has(f)`, `nonempty(f)`, `"x" in f`,
        `f ~ "re"`, `f = "s"`, `f >= 3`, ...; empty always holds.
    payload: The fields the predicate reads; need not belong to a tracked document.
    subject: Fills `{field}` placeholders (default: `payload`). A placeholder the subject
        lacks, or holds as a list or dict, makes the expression not hold.

Raises:
    WherePredicateError: No evaluator parses some part of the expression.

## Imports

["__future__", "sldb.store.query_engine.where_subject", "typing"]

## Purpose

Whether a `--where` predicate holds on `payload` (the grammar of `sldb find --where`).

## Architecture

Not documented.
