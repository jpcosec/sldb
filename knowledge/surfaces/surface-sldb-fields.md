---
id: surface-sldb-fields
system: sldb
surface: fields
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: src/sldb/cli/parsers/
---

# fields

## Purpose

Field inspection and mutation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'fields' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

fields show
fields query
fields create
fields update
fields remove
fields append
fields clean
