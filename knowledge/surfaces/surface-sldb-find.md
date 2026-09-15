---
id: surface-sldb-find
system: sldb
surface: find
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#find; contract-sha256:e0bfe85dcee0770390b76e464421537d2ef4afbf9d7d25e9ef214e5ff15bc22f
---

# find

## Purpose

Unified semantic + physical retrieval. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'find' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb find
