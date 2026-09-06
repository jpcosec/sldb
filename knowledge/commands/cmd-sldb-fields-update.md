---
id: cmd-sldb-fields-update
system: sldb
command_path: fields update
synopsis: Update
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# fields update

## Synopsis

Update

## Purpose

The `sldb fields update` command: Update

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'update'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | required | docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>
value | required | Inline YAML/JSON value
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

fields update
