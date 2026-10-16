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
provenance: parser:sldb.cli.parser:build_parser#docs; contract-sha256:e8cadc49f4389387abcdf9fb27c1abd54b900d56b9b0e33492903e37de5c0408
---

# docs

## Purpose

Tracked document workflows. Groups 9 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'docs' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb docs compose
- sldb docs create
- sldb docs delete
- sldb docs exists
- sldb docs explore
- sldb docs list
- sldb docs recover
- sldb docs show
- sldb docs track
- sldb docs untrack
- sldb docs update
