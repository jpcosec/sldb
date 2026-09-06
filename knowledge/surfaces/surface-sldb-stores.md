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
provenance: src/sldb/cli/parsers/
---

# stores

## Purpose

Store lifecycle and federation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'stores' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

stores init
stores add
stores check
stores update
stores semantic-map
stores semantic-export
stores list
