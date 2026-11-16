---
sldb:
  by: agent
  at: '2026-11-16T20:53:51Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-init
system: sldb
surface: init
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#init; contract-sha256:9697092f003eaf68726658fa0a048c0430f11c9aa212e514bb15d6da968ded88
---

# init

## Purpose

Store bootstrapping helper. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'init' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb init
