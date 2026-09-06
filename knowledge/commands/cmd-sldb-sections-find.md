---
id: cmd-sldb-sections-find
system: sldb
command_path: sections find
synopsis: Search sections semantically or physically.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# sections find

## Synopsis

Search sections semantically or physically.

## Purpose

The `sldb sections find` command: Search sections semantically or physically.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'find'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

term | required | 
--in | optional | 
--store | optional | Store path
--pythonpath | optional | Project path
--global | optional | 
--regex | optional | 
--fuzzy | optional | 
--rebuild | optional | 
--where | optional | Section context predicate
--format | optional | 

## Usage

sections find
