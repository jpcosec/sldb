---
id: surface-sldb-init
system: sldb
surface: init
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#init; contract-sha256:74e0986dc3590370dc5c67a46bcef8cbe79f47792cb014b23d185c592e281d6f
---

# init

## Purpose

Store bootstrapping helper. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'init' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb init
