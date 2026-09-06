---
id: cmd-sldb-stores-add
system: sldb
command_path: stores add
synopsis: Link federated store.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores add

## Synopsis

Link federated store.

## Purpose

The `sldb stores add` command: Link federated store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'add'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

path | required | Store path
--name | optional | Store name
--store | optional | Local store path

## Usage

stores add
