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
provenance: parser:sldb.cli.parser:build_parser#lint; contract-sha256:3e592c55f7905f39606c20f99f4056182a64aeecafa22acd438c662442d52939
---

# lint

## Purpose

Lint tracked documents. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'lint' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb lint
