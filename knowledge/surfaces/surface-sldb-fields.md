---
sldb:
  by: agent
  at: '2026-11-16T20:49:20Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-fields
system: sldb
surface: fields
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#fields; contract-sha256:634c16c8d1a91e81cda8a26c9ecd8ba144d650de8ab1ddd2d93edfb559fc2b11
---

# fields

## Purpose

Field inspection and mutation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'fields' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb fields append
- sldb fields clean
- sldb fields create
- sldb fields query
- sldb fields remove
- sldb fields show
- sldb fields update
