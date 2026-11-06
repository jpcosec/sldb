---
sldb:
  by: agent
  at: '2026-11-06T20:45:01Z'
  authority: generated
  via: save_document_payload
id: surface-sldb-models
system: sldb
surface: models
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_surface
provenance: parser:sldb.cli.parser:build_parser#models; contract-sha256:d5ff7eecb808896f02714d6ec2072b108d724bc6e1c77f5bcb08d48da2731ad5
---

# models

## Purpose

Model contracts and code generation. Groups 10 command(s).

## How It Works

Registered under src/sldb/cli/parsers/ as the 'models' subparser. Each command dispatches to its handler over the .sldb store.

## Commands

- sldb models add
- sldb models check
- sldb models create
- sldb models fields add
- sldb models fields remove
- sldb models inherit
- sldb models list
- sldb models metadata edit
- sldb models remove
- sldb models show
- sldb models template edit
- sldb models template show
- sldb models update
- sldb models validate
