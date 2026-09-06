---
id: cmd-sldb-sections-show
system: sldb
command_path: sections show
synopsis: Show sections in a document.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# sections show

## Synopsis

Show sections in a document.

## Purpose

The `sldb sections show` command: Show sections in a document.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

doc | required | Doc name or Model/DocName
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 

## Usage

sections show
