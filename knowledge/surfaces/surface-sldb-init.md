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
provenance: src/sldb/cli/parsers/
---

# init

## Purpose

Store bootstrapping helper. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'init' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

init
