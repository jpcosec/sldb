---
id: surface-sldb-validate
system: sldb
surface: validate
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: src/sldb/cli/parsers/
---

# validate

## Purpose

Validate idempotency. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'validate' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

validate
