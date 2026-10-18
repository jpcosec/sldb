---
id: python-sldb-sldb-cli-serve-corpus_routes-corpus_rank
system: sldb
module: sldb.cli.serve.corpus_routes
qualname: corpus_rank
kind: FunctionDef
source_path: sldb/cli/serve/corpus_routes.py
source_span: '21:40'
source_sha256: fc8fd01acab0e9a2ff9c25941ec02c04fc31ad15b72c230538fca63de614b895
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.corpus_routes:corpus_rank; contract-sha256:5b9edcea1b8cd89d694ee2a00f5c3fc6cafebb1fccf4be68a36ce4e6b2c3f8bf
---

# corpus_rank

## Signature

corpus_rank(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str)

## Docstring

Serve `?q=&k=&threshold=&among=&fields=&refresh=`.

Returns `{"hits": [Hit...]}` (or `[FieldHit...]` with `fields=1`) and 200; 400 for a
missing or invalid parameter; 409 `{"ok": false, "error": "corpus no indexado",
"kind": "not_indexed"}` when the index does not exist yet and `refresh` is off.

`refresh=0` (default) only reads the index: it never embeds or writes, so it is fast, and it
ranks what was indexed last (documents added since are not found until a refresh).
`refresh=1` runs `refresh_if_stale`: it builds the index when absent and re-embeds only what
drifted, so the call that does it can be slow. An empty `hits` always means "no matches".

## Imports

["__future__", "dataclasses", "http.server", "pathlib", "pydantic", "sldb.api.corpus.corpus", "sldb.cli.serve.corpus_projection", "sldb.cli.serve.params", "sldb.cli.serve.rank_request", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
