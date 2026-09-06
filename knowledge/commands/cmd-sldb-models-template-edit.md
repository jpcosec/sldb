---
id: cmd-sldb-models-template-edit
system: sldb
command_path: models template edit
synopsis: Write a template draft for a registered model.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models template edit

## Synopsis

Write a template draft for a registered model.

## Purpose

The `sldb models template edit` command: Write a template draft for a registered model.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'edit'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
--input | required | Template markdown path
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

models template edit
