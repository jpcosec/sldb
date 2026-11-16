---
sldb:
  by: agent
  at: '2026-11-16T20:44:18Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-ast
system: sldb
surface: ast
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#ast; contract-sha256:02cc829aedc665147bd804e328355167190d4ff2e579abe18233d73bf2da8f00
---

# ast

## Purpose

Normalized store/model/document graph. Groups 2 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'ast' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb ast schema
- sldb ast show
