---
id: cmd-sldb-models-add
system: sldb
command_path: models add
synopsis: Register model.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models add

## Synopsis

Register model.

## Purpose

The `sldb models add` command: Register model.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'add'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model ref
--store | optional | Store path
--pythonpath | optional | Project path
--canonical | optional | 

## Usage

models add
