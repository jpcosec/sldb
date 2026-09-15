---
id: surface-sldb-fields
system: sldb
surface: fields
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#fields; contract-sha256:8748c1d008f374e5692b73fd8189b12c0eac20a8a5c46ffed67c95c7524ad132
---

# fields

## Purpose

Field inspection and mutation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'fields' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb fields append
- sldb fields clean
- sldb fields create
- sldb fields query
- sldb fields remove
- sldb fields show
- sldb fields update
