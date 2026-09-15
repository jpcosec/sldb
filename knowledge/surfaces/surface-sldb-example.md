---
id: surface-sldb-example
system: sldb
surface: example
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#example; contract-sha256:a79207ee248dc6268dcdffa7431d62e7825f5eaee5bb3a5c50f26f499f072125
---

# example

## Purpose

Ship example bundle. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'example' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb example
