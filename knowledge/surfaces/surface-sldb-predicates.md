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
provenance: parser:sldb.cli.parser:build_parser#predicates; contract-sha256:ad418d3431da794c9221921b7e8af339e1604bc404323efb5aa260284ad753bf
---

# predicates

## Purpose

Store-backed semantic link predicates. Groups 5 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'predicates' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb predicates add
- sldb predicates export
- sldb predicates list
- sldb predicates remove
- sldb predicates show
- sldb predicates sync
- sldb predicates validate
