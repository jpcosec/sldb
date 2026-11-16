---
sldb:
  by: agent
  at: '2026-11-16T20:48:17Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-example
system: sldb
surface: example
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#example; contract-sha256:28e34d9fa377fb466bb21992bf82ce49af035e191c27a4b92009adb917236f79
---

# example

## Purpose

Ship example bundle. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'example' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb example
