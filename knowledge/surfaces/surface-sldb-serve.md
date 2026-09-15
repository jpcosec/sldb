---
id: surface-sldb-serve
system: sldb
surface: serve
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#serve; contract-sha256:8870c19f460bf1dd636e7c56d19b084013febc33b8efc31c81c0641fcc6b6b1d
---

# serve

## Purpose

HTTP transport over the store. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'serve' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb serve
