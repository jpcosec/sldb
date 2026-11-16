---
sldb:
  by: agent
  at: '2026-11-16T20:50:32Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-find
system: sldb
surface: find
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#find; contract-sha256:cfa06f6241aa64d72a366460bcb3bed7c43f486fd2c84e86daa9ad54f84c385c
---

# find

## Purpose

Unified semantic + physical retrieval. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'find' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb find
