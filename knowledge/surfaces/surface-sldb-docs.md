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
provenance: parser:sldb.cli.parser:build_parser#docs; contract-sha256:25b67a7665ddc2e3c6f88ea280f36c23d46bd2e99823c7346a9c6e149be97edb
---

# docs

## Purpose

Tracked document workflows. Groups 9 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'docs' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb docs compose
- sldb docs create
- sldb docs explore
- sldb docs list
- sldb docs recover
- sldb docs show
- sldb docs track
- sldb docs untrack
- sldb docs update
