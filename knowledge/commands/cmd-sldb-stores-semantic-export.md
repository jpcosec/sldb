---
id: cmd-sldb-stores-semantic-export
system: sldb
command_path: stores semantic-export
synopsis: Export semantic payloads.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores semantic-export

## Synopsis

Export semantic payloads.

## Purpose

The `sldb stores semantic-export` command: Export semantic payloads.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'semantic-export'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 
--encoding | optional | 
--output | optional | Output path or -
--rebuild | optional | Refresh semantic and section indexes

## Usage

stores semantic-export
