---
id: python-sldb-sldb-sldb-cli-serve-similar_routes-similar_payload
system: sldb
module: sldb.sldb.cli.serve.similar_routes
qualname: similar_payload
kind: FunctionDef
source_path: sldb/cli/serve/similar_routes.py
source_span: '14:32'
source_sha256: f8b16e4745358ba65be7fa12946659c0b1c122677a6f06b7e0b7bae601dc1572
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.similar_routes:similar_payload;
  contract-sha256:c591f386a7027016e52894b67a5b624e3cb7c97adc776e30969b09a572b4706d
---

# similar_payload

## Signature

similar_payload(handler: BaseHTTPRequestHandler, store_path: Path)

## Docstring

Serve `?id=&relations=&limit=&types=`.

`id` is a node id (`sldb://document/Model:name`) or an export id (`Model:name`); `relations`
defaults to `tagged_as`, `types` filters the answer by node class (e.g. `NoteDoc`).
Returns `{"similar": [[node_id, shared_targets], ...]}` (most shared first, ties by id,
exactly what `similar_to` returns) and 200; 400 without `id` or with a bad `limit`;
404 when the store has no such node. An empty list means "nothing resembles it".

## Imports

["__future__", "http.server", "pathlib", "sldb.api.edges.edge_reading", "sldb.api.graph.analyze", "sldb.cli.serve.params", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
