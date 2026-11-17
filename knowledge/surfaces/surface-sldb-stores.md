---
sldb:
  by: agent
  at: '2026-11-17T00:23:41Z'
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
provenance: parser:sldb.cli.parser:build_parser#stores; contract-sha256:072bd44ee824eca49bacc3f47d703f9a1f60ce6f1f6482456496ddce32c9645b
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
- sldb stores merge-driver
- sldb stores migrate-hashes
- sldb stores migrate-layout
- sldb stores rebuild-index
- sldb stores reconcile
- sldb stores remove
- sldb stores scaffold
- sldb stores semantic-export
- sldb stores semantic-map
- sldb stores update
