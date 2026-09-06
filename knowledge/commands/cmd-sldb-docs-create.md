---
id: cmd-sldb-docs-create
system: sldb
command_path: docs create
synopsis: Create and track document.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs create

## Synopsis

Create and track document.

## Purpose

The `sldb docs create` command: Create and track document.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'create'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--model | required | 
-o | required | 
payload | required | Data file or inline YAML/JSON
--name | optional | Doc name
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

docs create
