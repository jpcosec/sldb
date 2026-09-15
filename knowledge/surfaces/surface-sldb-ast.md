---
id: surface-sldb-ast
system: sldb
surface: ast
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#ast; contract-sha256:8fb9d72ca813046a3598946dc3c3d07e5991b87247b646069496361f0c962837
---

# ast

## Purpose

Normalized store/model/document graph. Groups 2 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'ast' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb ast schema
- sldb ast show
