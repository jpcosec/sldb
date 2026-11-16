---
sldb:
  by: agent
  at: '2026-11-16T21:09:34Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-stores
system: sldb
surface: stores
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#stores; contract-sha256:b7c34da2ed8ce91171dcf2d8791e274228c4ba2f3f8019f3802d03c8cc8eee1d
---

# stores

## Purpose

Store lifecycle and federation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'stores' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb stores add
- sldb stores build
- sldb stores check
- sldb stores declare
- sldb stores init
- sldb stores list
- sldb stores migrate-hashes
- sldb stores migrate-layout
- sldb stores reconcile
- sldb stores remove
- sldb stores scaffold
- sldb stores semantic-export
- sldb stores semantic-map
- sldb stores update
