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
provenance: parser:sldb.cli.parser:build_parser#validate; contract-sha256:2c4c5cdfd763fd6eb1bb6644ea715f8d0296549ab46bd6073f9637a4b8d2974d
---

# validate

## Purpose

Validate idempotency. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'validate' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb validate
