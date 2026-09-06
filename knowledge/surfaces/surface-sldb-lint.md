---
id: surface-sldb-lint
system: sldb
surface: lint
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: src/sldb/cli/parsers/
---

# lint

## Purpose

Lint tracked documents. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'lint' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

lint
