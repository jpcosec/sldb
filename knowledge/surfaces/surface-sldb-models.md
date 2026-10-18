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
provenance: parser:sldb.cli.parser:build_parser#models; contract-sha256:6caea32399f799c92ea80644a4ba400027ce71153a6bbdae3ed248d35c79ff86
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
- sldb models remove
- sldb models show
- sldb models template edit
- sldb models template show
- sldb models update
- sldb models validate
