---
id: cmd-sldb-models-update
system: sldb
command_path: models update
synopsis: Update model hashes.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models update

## Synopsis

Update model hashes.

## Purpose

The `sldb models update` command: Update model hashes.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'update'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

models update
