---
id: python-sldb-sldb-cli-serve-docs_create_route-create_doc_response
system: sldb
module: sldb.cli.serve.docs_create_route
qualname: create_doc_response
kind: FunctionDef
source_path: sldb/cli/serve/docs_create_route.py
source_span: '23:37'
source_sha256: 79b73c7179904afcce55e13cb37594706aa5766a15727fd520ec042caafd7874
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.docs_create_route:create_doc_response;
  contract-sha256:64d74a2110643d1ff20aee4b5d27b5d12f3c1f9abf703d904efda47ca28cb6ae
---

# create_doc_response

## Signature

create_doc_response(handler: Any, store_path: Path, project_root: Path, pythonpath: str)

## Docstring

Create `{model, name, payload}` under the same lock /save uses.

Returns `{ok, id, version}` (200), or `{ok: false, error}` with 400 (malformed body
or name), 404 (model not registered), 409 (name taken) or 422 (invalid payload).

## Imports

["__future__", "pathlib", "sldb.cli.serve.docs_routes", "sldb.cli.serve.responses", "sldb.cli.serve.save_plan", "sldb.cli.serve.save_routes", "typing"]

## Purpose

Create `{model, name, payload}` under the same lock /save uses.

## Architecture

Not documented.
