---
id: cmd-sldb-fields-clean
system: sldb
command_path: fields clean
synopsis: Clean a list field.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# fields clean

## Synopsis

Clean a list field.

## Purpose

The `sldb fields clean` command: Clean a list field.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'clean'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | required | docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>
--store | optional | Store path
--pythonpath | optional | Project path
--dedupe | optional | 
--drop-empty | optional | 

## Usage

fields clean
