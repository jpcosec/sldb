---
id: python-sldb-sldb-cli-serve-edges_documents_routes-document_edges_payload
system: sldb
module: sldb.cli.serve.edges_documents_routes
qualname: document_edges_payload
kind: FunctionDef
source_path: sldb/cli/serve/edges_documents_routes.py
source_span: '28:31'
source_sha256: aaf7bc3cc997ce239341472eeb0d2b99eac11071164f41c70bf7aa896e291c99
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.edges_documents_routes:document_edges_payload;
  contract-sha256:8d9cbc1c46f33773215abc9a38af6f7e9432b5bdb9b326e07deaf901466d4712
---

# document_edges_payload

## Signature

document_edges_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str)

## Docstring

`{edges: [{id, source, target, type, origin, relationDoc}]}`, optionally for `?id=Model:name`.

## Imports

["__future__", "http.server", "pathlib", "sldb.api.edges.document_edges", "sldb.cli.serve.edges_routes", "sldb.cli.serve.params", "typing", "urllib.parse"]

## Purpose

`{edges: [{id, source, target, type, origin, relationDoc}]}`, optionally for `?id=Model:name`.

## Architecture

Not documented.
