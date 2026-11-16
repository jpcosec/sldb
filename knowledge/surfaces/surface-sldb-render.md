---
sldb:
  by: agent
  at: '2026-11-16T21:02:25Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-render
system: sldb
surface: render
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#render; contract-sha256:90766ef79e1d59b6b053022cb5cc72c7f39f6d0eae46edec0b3fea5ae73a2040
---

# render

## Purpose

Render Markdown from data. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'render' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb render
