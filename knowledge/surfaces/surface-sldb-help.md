---
id: surface-sldb-help
system: sldb
surface: help
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#help; contract-sha256:3a232bac71000b48414029113e6c0651e15a539fe9609d760f282d62fb6e89a7
---

# help

## Purpose

Curated first-use guidance. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'help' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb help
