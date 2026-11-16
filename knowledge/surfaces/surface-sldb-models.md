---
sldb:
  by: agent
  at: '2026-11-16T20:56:09Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-models
system: sldb
surface: models
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#models; contract-sha256:86591896dde13db8de86f717a312845d03a17fe5c0c8e4989e32e6448c40a050
---

# models

## Purpose

Model contracts and code generation. Groups 10 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'models' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb models add
- sldb models check
- sldb models create
- sldb models fields add
- sldb models fields remove
- sldb models inherit
- sldb models list
- sldb models metadata edit
- sldb models remove
- sldb models show
- sldb models template edit
- sldb models template show
- sldb models update
- sldb models validate
