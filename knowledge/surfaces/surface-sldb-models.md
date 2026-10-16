---
id: surface-sldb-models
system: sldb
surface: models
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#models; contract-sha256:80c3e253fbaabdb9d49cc3b167b4a4b789e7e48cc416a0041a2adbb4bdda7ee7
---

# models

## Purpose

Model contracts and code generation. Groups 10 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'models' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb models add
- sldb models create
- sldb models fields add
- sldb models fields remove
- sldb models list
- sldb models remove
- sldb models show
- sldb models template edit
- sldb models template show
- sldb models update
- sldb models validate
