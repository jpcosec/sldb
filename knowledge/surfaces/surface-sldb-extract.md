---
sldb:
  by: agent
  at: '2026-11-16T20:48:55Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-extract
system: sldb
surface: extract
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#extract; contract-sha256:a8b25c282a96dad4240383b7a334cd3f73d29f6993791c8d82b11669b5168d66
---

# extract

## Purpose

Extract data from Markdown. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'extract' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb extract
