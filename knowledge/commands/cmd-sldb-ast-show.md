---
id: cmd-sldb-ast-show
system: sldb
command_path: ast show
synopsis: Show AST for a target.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# ast show

## Synopsis

Show AST for a target.

## Purpose

The `sldb ast show` command: Show AST for a target.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | optional | 
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 

## Usage

ast show
