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
provenance: parser:sldb.cli.parser:build_parser#models; contract-sha256:9f518e03a6236384d309f13dc6e8628de221b30cd0641da2dc13a77fb1d92b28
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
- sldb models show
- sldb models template edit
- sldb models template show
- sldb models update
- sldb models validate
