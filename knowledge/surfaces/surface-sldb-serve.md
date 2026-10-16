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
provenance: parser:sldb.cli.parser:build_parser#serve; contract-sha256:5e0a5281eea874003c108026b2a999676f80d85a74106e8e7fe0dc4b2fac8f69
---

# serve

## Purpose

HTTP transport over the store. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'serve' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb serve
