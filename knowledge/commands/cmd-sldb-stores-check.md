---
id: cmd-sldb-stores-check
system: sldb
command_path: stores check
synopsis: Integrity check.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores check

## Synopsis

Integrity check.

## Purpose

The `sldb stores check` command: Integrity check.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'check'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--store | optional | Store path
--format | optional | 
--pythonpath | optional | Project path

## Usage

stores check
