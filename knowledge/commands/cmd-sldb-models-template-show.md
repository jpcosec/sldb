---
id: cmd-sldb-models-template-show
system: sldb
command_path: models template show
synopsis: Show the active or draft template.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models template show

## Synopsis

Show the active or draft template.

## Purpose

The `sldb models template show` command: Show the active or draft template.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
--store | optional | Store path
--pythonpath | optional | Project path
--draft | optional | Show the draft template

## Usage

models template show
