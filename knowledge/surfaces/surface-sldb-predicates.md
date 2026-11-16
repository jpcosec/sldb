---
sldb:
  by: agent
  at: '2026-11-16T21:00:22Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-predicates
system: sldb
surface: predicates
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#predicates; contract-sha256:daa0382ab3efaf9701bcd06a2a7640ba03b7658635216effef93d2ce24a84934
---

# predicates

## Purpose

Store-backed semantic link predicates. Groups 5 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'predicates' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb predicates add
- sldb predicates export
- sldb predicates list
- sldb predicates remove
- sldb predicates show
- sldb predicates sync
- sldb predicates validate
