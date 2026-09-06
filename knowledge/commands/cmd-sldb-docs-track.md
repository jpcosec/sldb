---
id: cmd-sldb-docs-track
system: sldb
command_path: docs track
synopsis: Track existing doc.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs track

## Synopsis

Track existing doc.

## Purpose

The `sldb docs track` command: Track existing doc.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'track'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

path | required | Document path
--model | required | 
--name | optional | Doc name
--store | optional | Store path
--pythonpath | optional | Project path
--force | optional | 

## Usage

docs track
