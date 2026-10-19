---
id: python-sldb-sldb-api-matching-matcher-matcher-rank
system: sldb
module: sldb.api.matching.matcher
qualname: Matcher.rank
kind: FunctionDef
source_path: sldb/api/matching/matcher.py
source_span: 47:60
source_sha256: 7334a378c54f363ba71d8ff8b2cc7c745b0829982ea43482513a209000ccd0be
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.matching.matcher:Matcher.rank; contract-sha256:6dc9e175bb5ee9fb68a3d33a79eb1ca75cc79925e9bec090e44d4712fdce07f0
---

# Matcher.rank

## Signature

rank(self, query: str, candidates: Sequence[tuple[str, str]], k: int=3, threshold: float=0.0)

## Docstring

candidates are (key, text). Returns [(key, score)] best first, above threshold.

## Imports

["__future__", "json", "math", "pathlib", "sldb.api.matching.difflib_matcher", "sldb.api.matching.embedder_protocol", "typing"]

## Purpose

candidates are (key, text). Returns [(key, score)] best first, above threshold.

## Architecture

Not documented.
