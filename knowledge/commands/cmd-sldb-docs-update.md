---
id: cmd-sldb-docs-update
system: sldb
command_path: docs update
synopsis: Update doc content.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs update

## Synopsis

Update doc content.

## Purpose

The `sldb docs update` command: Update doc content.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'update'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

doc | required | Doc name or path
payload | required | Data file or inline YAML/JSON
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

docs update
