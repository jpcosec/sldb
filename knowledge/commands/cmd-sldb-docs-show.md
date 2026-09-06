---
id: cmd-sldb-docs-show
system: sldb
command_path: docs show
synopsis: Show document AST and payload.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs show

## Synopsis

Show document AST and payload.

## Purpose

The `sldb docs show` command: Show document AST and payload.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

doc | required | Doc name or Model/DocName or tracked path
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 

## Usage

docs show
