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
provenance: src/sldb/cli/parsers/
---

# serve

## Purpose

HTTP transport over the store. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'serve' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

serve
