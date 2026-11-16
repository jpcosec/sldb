---
sldb:
  by: agent
  at: '2026-11-16T20:53:34Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-inbox
system: sldb
surface: inbox
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#inbox; contract-sha256:86f7c85a69ff1c87a3fde7cada1a131a181e20f8faaa7fe9ff2eb1025e3f15f4
---

# inbox

## Purpose

Log unclear points or suggestions. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'inbox' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb inbox
