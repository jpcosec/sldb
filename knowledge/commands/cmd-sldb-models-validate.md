---
id: cmd-sldb-models-validate
system: sldb
command_path: models validate
synopsis: Validate a registered model or draft.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models validate

## Synopsis

Validate a registered model or draft.

## Purpose

The `sldb models validate` command: Validate a registered model or draft.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'validate'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
--store | optional | Store path
--pythonpath | optional | Project path
--promote | optional | Promote a valid draft
--format | optional | 

## Usage

models validate
