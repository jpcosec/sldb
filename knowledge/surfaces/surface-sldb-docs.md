---
sldb:
  by: agent
  at: '2026-10-20T16:30:17Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-docs
system: sldb
surface: docs
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#docs; contract-sha256:8c69e8b0f9a0d4f868262aeb3934409fea2f31bd331307a9c84d4f33d3e7088a
---

# docs

## Purpose

Tracked document workflows. Groups 9 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'docs' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb docs compose
- sldb docs create
- sldb docs delete
- sldb docs exists
- sldb docs explore
- sldb docs history
- sldb docs list
- sldb docs recover
- sldb docs show
- sldb docs track
- sldb docs untrack
- sldb docs update
