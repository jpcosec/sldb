---
sldb:
  by: agent
  at: '2026-11-16T21:04:59Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-sections
system: sldb
surface: sections
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#sections; contract-sha256:f4f3f3d9a663d194f20143fcffb876bd308c07f46dd4070335dd316facd34985
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
