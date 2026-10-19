---
id: python-sldb-sldb-cli-commands-docs_batch-track_glob
system: sldb
module: sldb.cli.commands.docs_batch
qualname: track_glob
kind: FunctionDef
source_path: sldb/cli/commands/docs_batch.py
source_span: '17:27'
source_sha256: 74cfb6791eec653396bc7b3da0b3826ab0c51d9e1e65c52fcfaef46828579330
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.commands.docs_batch:track_glob; contract-sha256:392de90a77af07bfdf230787a3bcd9f7b01f529d974ee155f10b87b37e350f2e
---

# track_glob

## Signature

track_glob(args: Any)

## Docstring

Track every file matching `args.glob`; the ones already tracked are skipped.

## Imports

["__future__", "glob", "pathlib", "sldb.api.documents.track_document_file", "sldb.api.documents.untrack_document", "sldb.cli.store_context", "sldb.core.exceptions", "sldb.links.tracked", "typing"]

## Purpose

Track every file matching `args.glob`; the ones already tracked are skipped.

## Architecture

Not documented.
