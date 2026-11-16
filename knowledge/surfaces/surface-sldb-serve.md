---
sldb:
  by: agent
  at: '2026-11-16T21:09:23Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-serve
system: sldb
surface: serve
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#serve; contract-sha256:25aaa58a6e903fef60aa57fc24fa271df72f3fdad0c0cbb0097f704dd18c3dd5
---

# serve

## Purpose

HTTP transport over the store. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'serve' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb serve
