---
id: surface-sldb-predicates
system: sldb
surface: predicates
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: src/sldb/cli/parsers/
---

# predicates

## Purpose

Store-backed semantic link predicates. Groups 5 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'predicates' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

predicates add
predicates list
predicates show
predicates validate
predicates remove
