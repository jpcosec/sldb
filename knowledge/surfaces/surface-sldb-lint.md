---
sldb:
  by: agent
  at: '2026-11-16T20:55:41Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-lint
system: sldb
surface: lint
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#lint; contract-sha256:d6f5a58f282387f65533ac029658b88c5f9b369a61000197125b881f1172e879
---

# lint

## Purpose

Lint tracked documents. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'lint' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb lint
