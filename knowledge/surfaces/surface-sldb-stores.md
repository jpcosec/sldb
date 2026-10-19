---
id: surface-sldb-stores
system: sldb
surface: stores
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#stores; contract-sha256:777e23f7fa393e82f7c2b39b6756fa516c408edbe83858404095f53134de72b0
---

# stores

## Purpose

Store lifecycle and federation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'stores' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb stores add
- sldb stores build
- sldb stores check
- sldb stores declare
- sldb stores init
- sldb stores list
- sldb stores migrate-hashes
- sldb stores reconcile
- sldb stores remove
- sldb stores semantic-export
- sldb stores semantic-map
- sldb stores update
