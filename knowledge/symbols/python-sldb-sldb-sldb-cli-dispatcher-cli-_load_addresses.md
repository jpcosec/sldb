---
id: python-sldb-sldb-sldb-cli-dispatcher-cli-_load_addresses
system: sldb
module: sldb.sldb.cli.dispatcher
qualname: CLI._load_addresses
kind: FunctionDef
source_path: sldb/cli/dispatcher.py
source_span: '45:57'
source_sha256: 53357ad6f727e63011b4517f0e20555413669b91354668492cff9273cf1604ae
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.cli.dispatcher:CLI._load_addresses; contract-sha256:e6ec98f80d81b32fd3bf97605dc477eb427569258d334950304e0306786913ee
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

["__future__", "sldb.cli.commands.help_texts", "sldb.cli.parser", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
