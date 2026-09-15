---
id: surface-sldb-extract
system: sldb
surface: extract
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#extract; contract-sha256:8360e64bc232e35fbd51c401ac68c69939596417a52cc3972fcaa81dc59ee8f2
---

# extract

## Purpose

Extract data from Markdown. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'extract' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb extract
