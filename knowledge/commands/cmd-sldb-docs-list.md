---
id: cmd-sldb-docs-list
system: sldb
command_path: docs list
synopsis: List tracked documents.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs list

## Synopsis

List tracked documents.

## Purpose

The `sldb docs list` command: List tracked documents.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'list'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--store | optional | Store path
--format | optional | 

## Usage

docs list
