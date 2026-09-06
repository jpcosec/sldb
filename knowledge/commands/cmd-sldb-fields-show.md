---
id: cmd-sldb-fields-show
system: sldb
command_path: fields show
synopsis: Show model field schema or document field value.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# fields show

## Synopsis

Show model field schema or document field value.

## Purpose

The `sldb fields show` command: Show model field schema or document field value.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | required | models/<Model>[/field] or docs/<Doc>/<field>
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 

## Usage

fields show
