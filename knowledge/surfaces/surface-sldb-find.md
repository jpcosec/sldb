---
sldb:
  by: agent
  at: '2026-11-06T20:44:59Z'
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
provenance: parser:sldb.cli.parser:build_parser#find; contract-sha256:d7641f6337c1fab6a753be7c7f4a1449f95e43a75787d5275294d1c23d8b446f
---

# find

## Purpose

Unified semantic + physical retrieval. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'find' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb find
