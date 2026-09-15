---
id: surface-sldb-stores
system: sldb
surface: stores
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#stores; contract-sha256:f69d5af091f96a41b632dbbdf690f23ddcf94ab1e3aa23ecf9049050b242a292
---

# stores

## Purpose

Store lifecycle and federation. Groups 7 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'stores' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb stores add
- sldb stores check
- sldb stores init
- sldb stores list
- sldb stores reconcile
- sldb stores semantic-export
- sldb stores semantic-map
- sldb stores update
