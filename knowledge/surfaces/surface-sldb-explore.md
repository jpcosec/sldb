---
sldb:
  by: agent
  at: '2026-11-16T20:48:33Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-explore
system: sldb
surface: explore
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#explore; contract-sha256:a0207a032b822c7ef490bf1d13acce579098b08815eefbb15d465a397bc5d9ed
---

# explore

## Purpose

Deep markdown docs and docstring search. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'explore' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb explore
