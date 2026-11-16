---
sldb:
  by: agent
  at: '2026-11-16T20:49:12Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-faq
system: sldb
surface: faq
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#faq; contract-sha256:d4e29ba122449ae36773c7bec1db755c2fd32af56c40fb6736f50e1edfba0d46
---

# faq

## Purpose

Question-oriented onboarding answers. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'faq' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb faq
