---
id: python-sldb-sldb-cli-dispatcher-cli-_load_addresses
system: sldb
module: sldb.cli.dispatcher
qualname: CLI._load_addresses
kind: FunctionDef
source_path: sldb/cli/dispatcher.py
source_span: 60:72
source_sha256: 215856cb5578fef5bd8328d3dd0a5936115496fa43415f224f000ef96c0d483f
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.dispatcher:CLI._load_addresses; contract-sha256:0838bffc10abf9421acb9f1209ba98eb2b7462e419b8204e0c2c2a734adef11c
---

# CLI._load_addresses

## Signature

_load_addresses(self)

## Docstring

The raw address surface: `legacy ls|get|glob|find|recover|compose`.

Addresses are `st.{Model}.doc.field` (structural), `se.tag` (semantic) and
`gse.tag` (global semantic). The singular top-level aliases (`ls`, `get`,
`glob`, `raw-find`, `recover`, `compose`) are the pre-redesign spelling and
route to the same handler.

## Imports

["__future__", "sldb.cli.commands.help_texts", "sldb.cli.parser", "sldb.cli.singular_handlers", "sldb.cli.subcommand_errors", "typing"]

## Purpose

The raw address surface: `legacy ls|get|glob|find|recover|compose`.

## Architecture

Not documented.
