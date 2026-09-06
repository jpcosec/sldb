---
id: cmd-sldb-models-show
system: sldb
command_path: models show
synopsis: Show registered model info.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models show

## Synopsis

Show registered model info.

## Purpose

The `sldb models show` command: Show registered model info.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

models show
