---
id: surface-sldb-render
system: sldb
surface: render
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#render; contract-sha256:e04642ea74565f1edd927135c01b15befc97e4c91cb83b4a44e861720e075743
---

# render

## Purpose

Render Markdown from data. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'render' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb render
