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
provenance: parser:sldb.cli.parser:build_parser#predicates; contract-sha256:09dee550a8545677adbcc0316279ed272343293c37123c2ca6534f94d0241940
---

# predicates

## Purpose

Store-backed semantic link predicates. Groups 5 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'predicates' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb predicates add
- sldb predicates list
- sldb predicates remove
- sldb predicates show
- sldb predicates validate
