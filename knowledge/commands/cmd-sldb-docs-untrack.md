---
id: cmd-sldb-docs-untrack
system: sldb
command_path: docs untrack
synopsis: Remove a tracked doc from the store.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs untrack

## Synopsis

Remove a tracked doc from the store.

## Purpose

The `sldb docs untrack` command: Remove a tracked doc from the store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'untrack'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

doc | required | Doc name or tracked path
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

docs untrack
