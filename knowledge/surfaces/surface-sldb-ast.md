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
provenance: src/sldb/cli/parsers/
---

# ast

## Purpose

Normalized store/model/document graph. Groups 2 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'ast' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

ast show
ast schema
