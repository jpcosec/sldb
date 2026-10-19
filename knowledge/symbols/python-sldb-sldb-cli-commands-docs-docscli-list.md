---
id: python-sldb-sldb-cli-commands-docs-docscli-list
system: sldb
module: sldb.cli.commands.docs
qualname: DocsCLI.list
kind: FunctionDef
source_path: sldb/cli/commands/docs.py
source_span: '46:55'
source_sha256: 693d414cf63105d4c72ef6d59da92358d862ee604ecc1953505ac8af59c40358
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.commands.docs:DocsCLI.list; contract-sha256:252a0d7a375c2594441e1ae45933f955bba92d7d7950e9d3181b0791a75738ab
---

# DocsCLI.list

## Signature

list(self, args: Any)

## Docstring

List tracked documents in the store.
Args:
    args (Any): CLI args.
Returns:
    int: Exit code.

## Imports

["__future__", "json", "sldb.api.stores.indexed_documents", "sldb.cli.commands.doc", "sldb.cli.commands.docs_exists", "sldb.cli.commands.explore", "sldb.cli.commands.links", "sldb.cli.graph_ops", "sldb.cli.store_context", "typing", "yaml"]

## Purpose

List tracked documents in the store. Args: args (Any): CLI args. Returns: int: Exit code.

## Architecture

Not documented.
