---
id: python-sldb-sldb-cli-serve-auth-resolve_token
system: sldb
module: sldb.cli.serve.auth
qualname: resolve_token
kind: FunctionDef
source_path: sldb/cli/serve/auth.py
source_span: '25:28'
source_sha256: 6bf049261c2e5a2c8b1fd0f49d97f1ab349357075937c5a4593b9a15cc51f876
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.auth:resolve_token; contract-sha256:32af69b1b95c1adff8669272a2254bab2bfc40a75942da5c4ed9540bf988f095
---

# resolve_token

## Signature

resolve_token(flag_value: str | None)

## Docstring

The CLI flag wins over the env var; empty or missing means no auth.

## Imports

["__future__", "hmac", "http.server", "os"]

## Purpose

The CLI flag wins over the env var; empty or missing means no auth.

## Architecture

Not documented.
