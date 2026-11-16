---
sldb:
  by: agent
  at: '2026-11-16T21:13:20Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-validate
system: sldb
surface: validate
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#validate; contract-sha256:fdb252b7bc859b5238a072d59614c4d5bb4867ed481cb7e4618a5b34702606a3
---

# validate

## Purpose

Validate idempotency. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'validate' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb validate
