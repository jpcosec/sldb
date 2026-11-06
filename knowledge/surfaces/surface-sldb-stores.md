---
sldb:
  by: agent
  at: '2026-11-06T20:45:09Z'
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
provenance: parser:sldb.cli.parser:build_parser#stores; contract-sha256:110c141700233abd497b98ccc2ba1adc2dacfb9841efa3981b1f2b3e95d8b2f7
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
- sldb stores semantic-export
- sldb stores semantic-map
- sldb stores update
