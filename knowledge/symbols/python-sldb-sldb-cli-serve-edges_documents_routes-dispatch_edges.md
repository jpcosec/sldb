---
id: python-sldb-sldb-cli-serve-edges_documents_routes-dispatch_edges
system: sldb
module: sldb.cli.serve.edges_documents_routes
qualname: dispatch_edges
kind: FunctionDef
source_path: sldb/cli/serve/edges_documents_routes.py
source_span: '15:19'
source_sha256: aaf7bc3cc997ce239341472eeb0d2b99eac11071164f41c70bf7aa896e291c99
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.edges_documents_routes:dispatch_edges;
  contract-sha256:db9fcbed4c80153a43f6e2342d5a87548135135eff3bbb0bd38bd613301a1817
---

# dispatch_edges

## Signature

dispatch_edges(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str)

## Docstring

Serve `/edges` bare or with `id` as the document view; `from`/`to`/`/edges/*` as before.

## Imports

["__future__", "http.server", "pathlib", "sldb.api.edges.document_edges", "sldb.cli.serve.edges_routes", "sldb.cli.serve.params", "typing", "urllib.parse"]

## Purpose

Serve `/edges` bare or with `id` as the document view; `from`/`to`/`/edges/*` as before.

## Architecture

Not documented.
