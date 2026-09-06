---
id: cmd-sldb-fields-append
system: sldb
command_path: fields append
synopsis: Append
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# fields append

## Synopsis

Append

## Purpose

The `sldb fields append` command: Append

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'append'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | required | docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>
value | required | Inline YAML/JSON value
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

fields append
