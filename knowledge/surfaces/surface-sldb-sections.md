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
provenance: src/sldb/cli/parsers/
---

# sections

## Purpose

Section context and navigation. Groups 3 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'sections' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

sections show
sections find
sections fields
