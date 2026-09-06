---
id: cmd-sldb-ast-schema
system: sldb
command_path: ast schema
synopsis: Show node and edge schema.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# ast schema

## Synopsis

Show node and edge schema.

## Purpose

The `sldb ast schema` command: Show node and edge schema.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'schema'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--format | optional | 

## Usage

ast schema
