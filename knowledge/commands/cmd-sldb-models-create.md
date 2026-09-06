---
id: cmd-sldb-models-create
system: sldb
command_path: models create
synopsis: Generate a StructuredNLDoc model.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models create

## Synopsis

Generate a StructuredNLDoc model.

## Purpose

The `sldb models create` command: Generate a StructuredNLDoc model.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'create'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

name | required | Class name
--template | required | Template markdown path
--fields | required | Field spec YAML path
--output | optional | Output Python file or -
--stdout | optional | Print generated code

## Usage

models create
