---
id: surface-sldb-sections
system: sldb
surface: sections
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#sections; contract-sha256:d5376952526324801076d5cd834650c453fcfdae72fc4079118589ab8f1e9aea
---

# sections

## Purpose

Section context and navigation. Groups 3 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'sections' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb sections fields
- sldb sections find
- sldb sections show
