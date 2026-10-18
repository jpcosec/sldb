---
id: python-sldb-sldb-sldb-cli-serve-docs_create_route-create_doc_response
system: sldb
module: sldb.sldb.cli.serve.docs_create_route
qualname: create_doc_response
kind: FunctionDef
source_path: sldb/cli/serve/docs_create_route.py
source_span: '23:37'
source_sha256: 79b73c7179904afcce55e13cb37594706aa5766a15727fd520ec042caafd7874
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.docs_create_route:create_doc_response;
  contract-sha256:722d91256c48bc7cb34ae0aeb6f728f9d775b4889e74de1ce4940dbbcf4d173b
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

Not documented.

## Architecture

Not documented.
