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
provenance: parser:sldb.cli.parser:build_parser#render; contract-sha256:f291623e696b9043083c7c4aaa335ec1ac274015aae782062e2ff6cf6a096fb7
---

# render

## Purpose

Render Markdown from data. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'render' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb render
