---
id: python-sldb-sldb-cli-serve-rank_request-rankrequest-split_among
system: sldb
module: sldb.cli.serve.rank_request
qualname: RankRequest.split_among
kind: FunctionDef
source_path: sldb/cli/serve/rank_request.py
source_span: '24:28'
source_sha256: 62a5c2ccdd125728448c0912853c63186117bfbfc614137aa9457d83dd236bf3
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.rank_request:RankRequest.split_among;
  contract-sha256:271290a6b29862995fd0b68162d9adc52047634bceb065dc12aafda548da9bf3
---

# RankRequest.split_among

## Signature

split_among(cls, value: Any)

## Docstring

`a,b` becomes `["a", "b"]`; blank items are dropped and an empty list means no filter.

## Imports

["__future__", "pydantic", "typing"]

## Purpose

`a,b` becomes `["a", "b"]`; blank items are dropped and an empty list means no filter.

## Architecture

Not documented.
