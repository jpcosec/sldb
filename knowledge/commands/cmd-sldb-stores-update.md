---
id: cmd-sldb-stores-update
system: sldb
command_path: stores update
synopsis: Recompute store hashes.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores update

## Synopsis

Recompute store hashes.

## Purpose

The `sldb stores update` command: Recompute store hashes.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'update'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--wait | optional | Wait for store lock if busy
--verbose | optional | Print individual skip details
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

stores update
