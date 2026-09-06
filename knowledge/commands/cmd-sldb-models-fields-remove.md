---
id: cmd-sldb-models-fields-remove
system: sldb
command_path: models fields remove
synopsis: Remove a field from the model draft.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models fields remove

## Synopsis

Remove a field from the model draft.

## Purpose

The `sldb models fields remove` command: Remove a field from the model draft.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'remove'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
field | required | Field name
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

models fields remove
