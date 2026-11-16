---
sldb:
  by: agent
  at: '2026-11-16T20:44:59Z'
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
provenance: parser:sldb.cli.parser:build_parser#docs; contract-sha256:0a7ecd38f8be077a8600e2c5f6d0a99c3c6972714023b00e781474818fa0c59d
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
- sldb docs replace
- sldb docs select
- sldb docs show
- sldb docs track
- sldb docs untrack
- sldb docs update
