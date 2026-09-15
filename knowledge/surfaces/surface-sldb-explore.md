---
id: surface-sldb-explore
system: sldb
surface: explore
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#explore; contract-sha256:a613761e9381bfba81be759c3d73d96bc020a8bc3adc8211be387b3b949bd905
---

# explore

## Purpose

Deep markdown docs and docstring search. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'explore' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb explore
