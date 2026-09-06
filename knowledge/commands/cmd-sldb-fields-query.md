---
id: cmd-sldb-fields-query
system: sldb
command_path: fields query
synopsis: Query a field path across tracked docs.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# fields query

## Synopsis

Query a field path across tracked docs.

## Purpose

The `sldb fields query` command: Query a field path across tracked docs.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'query'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

field | required | Field path, eg status or tasks.status
--store | optional | Store path
--pythonpath | optional | Project path
--global | optional | 
--format | optional | 

## Usage

fields query
