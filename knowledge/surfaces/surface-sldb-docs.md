---
sldb:
  by: agent
  at: '2026-11-15T20:04:55Z'
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
provenance: parser:sldb.cli.parser:build_parser#docs; contract-sha256:2e4c2075c30f4f187ec4a283a7695f1f10bd727ba36b290a11d22cc4e38e7cfe
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
