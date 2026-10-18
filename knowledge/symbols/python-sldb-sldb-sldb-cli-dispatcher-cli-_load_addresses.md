---
id: python-sldb-sldb-sldb-cli-dispatcher-cli-_load_addresses
system: sldb
module: sldb.sldb.cli.dispatcher
qualname: CLI._load_addresses
kind: FunctionDef
source_path: sldb/cli/dispatcher.py
source_span: 60:72
source_sha256: 215856cb5578fef5bd8328d3dd0a5936115496fa43415f224f000ef96c0d483f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.dispatcher:CLI._load_addresses; contract-sha256:c5a4092db106caa7a175904bd8c40111a7797cac7cb56c9f8ba0faa3ece24a78
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

Not documented.

## Architecture

Not documented.
