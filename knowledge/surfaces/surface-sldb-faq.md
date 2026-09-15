---
id: surface-sldb-faq
system: sldb
surface: faq
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#faq; contract-sha256:3142bc75631c1825e49076fe0fe8f0a9c54e3bb6c26ae705a0f7f516809242f9
---

# faq

## Purpose

Question-oriented onboarding answers. Groups 1 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'faq' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb faq
