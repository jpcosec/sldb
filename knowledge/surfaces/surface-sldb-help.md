---
sldb:
  by: agent
  at: '2026-11-16T20:53:16Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-help
system: sldb
surface: help
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#help; contract-sha256:881fa6ebe51dcbc3297882736fcef2bf0a7f8756ab90f5c89979b3ab617cee1c
---

# help

## Purpose

Curated first-use guidance. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'help' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb help
