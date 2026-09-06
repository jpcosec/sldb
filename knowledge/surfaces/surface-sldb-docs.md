---
id: surface-sldb-docs
system: sldb
surface: docs
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: src/sldb/cli/parsers/
---

# docs

## Purpose

Tracked document workflows. Groups 9 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'docs' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

docs create
docs track
docs update
docs untrack
docs show
docs recover
docs list
docs compose
docs explore
