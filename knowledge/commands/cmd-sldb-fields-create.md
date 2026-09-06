---
id: cmd-sldb-fields-create
system: sldb
command_path: fields create
synopsis: Create
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# fields create

## Synopsis

Create

## Purpose

The `sldb fields create` command: Create

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'create'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | required | docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>
value | required | Inline YAML/JSON value
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

fields create
