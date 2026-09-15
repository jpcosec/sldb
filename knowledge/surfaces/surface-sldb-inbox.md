---
id: surface-sldb-inbox
system: sldb
surface: inbox
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#inbox; contract-sha256:b37fc2b83589982b1a055c20bfd6530f3c12e39a9b782fc5064574784b15ec1c
---

# inbox

## Purpose

Log unclear points or suggestions. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'inbox' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb inbox
