---
id: cmd-sldb-stores-list
system: sldb
command_path: stores list
synopsis: List federated stores.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores list

## Synopsis

List federated stores.

## Purpose

The `sldb stores list` command: List federated stores.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'list'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--store | optional | Store path
--format | optional | 

## Usage

stores list
